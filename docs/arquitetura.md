# Padrões de arquitetura e de código

Este documento define como o software embarcado do projeto é organizado e escrito. Toda implementação nova em `src/presenca/` deve seguir estas regras. Se uma regra atrapalhar de verdade, mude o documento primeiro (e registre o motivo), em vez de abrir exceção silenciosa no código.

## 1. Visão geral

O sistema é um dispositivo **Edge AI / IoT**: reconhece os alunos no próprio ônibus e publica eventos de presença para o TRANSCOLAR RURAL. Os padrões adotados são:

| Problema | Padrão |
|---|---|
| Isolar a regra de negócio de bibliotecas (OpenCV, DeepFace, TFLite, Hailo, MQTT) | **Arquitetura hexagonal (Ports & Adapters)**, versão enxuta da Clean Architecture |
| Trocar o modelo de reconhecimento, a câmera ou o meio de envio (RNF-14) | **Strategy** atrás de uma porta (`typing.Protocol`) |
| Não perder nem duplicar eventos com rede instável (RF-07, RF-08) | **Store-and-forward / Outbox**: fila local em SQLite + MQTT QoS 1 + UUID por evento |
| Fluxo captura → reconhecimento → evento → envio | **Pipeline**: cada etapa é um componente separado |

Não adotamos: as quatro camadas completas da Clean Architecture, DTOs em cada fronteira, presenters, container de injeção de dependência, microsserviços no dispositivo. O sistema é pequeno (≈ 20 alunos por ônibus, uma desenvolvedora), e essas camadas só aumentariam o número de arquivos.

## 2. Estrutura de pastas

```
src/presenca/
  dominio/          # regras de negócio, Python puro
    modelos.py      #   Evento, TipoEvento, Identificacao
    passagens.py    #   ControlePassagens: decide embarque/desembarque/alerta
  portas.py         # Protocols: Camera, Reconhecedor, FilaEventos, Publicador, Relogio
  casos_uso/        # orquestram domínio + portas; um arquivo por caso de uso
    registrar_passagem.py
    sincronizar_eventos.py
  adaptadores/      # implementações concretas das portas (as únicas que importam libs externas)
  config.py         # leitura da configuração (TOML)
  __main__.py       # composition root: monta os objetos e roda o laço principal
tests/              # pytest; fakes das portas em tests/fakes.py
config/             # exemplos de configuração
```

O resto do repositório: `docs/` (documentação interna em Markdown, proposta e modelos do curso), `monografia/` (entregáveis LaTeX para o Overleaf: monografia e visão geral) e `pesquisa/` (experimentos).

**Nomes de arquivos e pastas:** minúsculas, sem espaços nem acentos, palavras separadas por `_`, em português. Datas no formato `AAAA-MM-DD`.

Os scripts de pesquisa ficam em `pesquisa/` (`preparar_dataset.py`, `benchmark_reconhecimento_facial.py`, `comparar_detectores.py`), com os datasets em `pesquisa/dados/` e as saídas em `pesquisa/resultados/`. Eles seguem os padrões de código, mas não a arquitetura em camadas (ver seção 8).

## 3. Regra de dependência

A dependência sempre aponta para dentro:

```
__main__  →  adaptadores  →  portas  ←  casos_uso  →  dominio
```

- `dominio/` não importa nada do projeto fora de `dominio/` e nenhuma biblioteca de terceiros. Só biblioteca padrão.
- `portas.py` importa apenas `dominio/`.
- `casos_uso/` importa `dominio/` e `portas.py`. **Nunca** importa `adaptadores/`, `cv2`, `deepface`, `paho`, `sqlite3` etc.
- `adaptadores/` implementam as portas e podem importar qualquer biblioteca. Bibliotecas pesadas (DeepFace, TensorFlow, cv2) são importadas **dentro** do construtor ou do método, para que o resto do pacote e os testes rodem sem elas.
- `__main__.py` é o único lugar que conhece todos os adaptadores concretos e os conecta aos casos de uso (injeção de dependência manual, pelo construtor).

## 4. Portas e adaptadores

- Portas são `typing.Protocol` pequenos (1 a 3 métodos). Não usar `abc.ABC` nem hierarquia de classes; o adaptador não precisa herdar da porta.
- Uma porta descreve **o que o domínio precisa**, não o que a biblioteca oferece. Ex.: `Reconhecedor.identificar(quadro) -> list[Identificacao]`, e não "rodar DeepFace.represent".
- Para trocar o modelo (ArcFace → Hailo, por exemplo), cria-se um adaptador novo; casos de uso e domínio não mudam (aberto/fechado).
- Toda porta tem um fake em `tests/fakes.py`, usado nos testes dos casos de uso.
- O tempo é uma porta (`Relogio`): casos de uso e domínio nunca chamam `datetime.now()` diretamente.

## 5. Regras específicas do domínio

- **LGPD (RF-05, RNF-07).** Nenhum adaptador grava imagem ou áudio bruto em disco, log ou rede. O quadro capturado vive só em memória durante o processamento. Logs nunca contêm o quadro nem o embedding.
- **Idempotência (RF-08).** Todo `Evento` nasce com um `id` UUID4, gerado no domínio. A fila local ignora `id` repetido, e o backend deve fazer o mesmo.
- **Store-and-forward (RF-07).** Todo evento é gravado primeiro na fila local; o envio é sempre feito a partir da fila pelo caso de uso `SincronizarEventos`. Nunca publicar direto sem passar pela fila.
- **Um evento só sai da fila depois do ACK** do broker (MQTT QoS 1), e sai **apagado**: o dispositivo guarda só o que ainda não foi enviado (RNF-16). Falha de envio não é erro fatal: o evento fica para a próxima sincronização.
- **Limiares e tempos** (confiança mínima, intervalo entre passagens, período de sincronização) vêm da configuração, nunca como número mágico no código.
- Datas e horários sempre com fuso (`datetime` *aware*, em UTC na serialização).

## 6. Padrões de código (Clean Code + SOLID)

- **Idioma:** identificadores, docstrings e comentários em português, como no restante do repositório. Termos técnicos consagrados podem ficar em inglês (`payload`, `broker`, `embedding`).
- **Nomes:** `snake_case` para funções, variáveis e módulos; `PascalCase` para classes; `MAIUSCULAS` para constantes. Casos de uso são classes com nome de verbo (`RegistrarPassagem`) e um método público `executar`.
- **Tipos:** type hints em toda função pública. Modelos de domínio são `@dataclass(frozen=True)` ou `Enum`.
- **Funções curtas, uma responsabilidade.** Se precisa de comentário explicando "agora faz X", vira função.
- **Comentários** explicam o *porquê*, não o *o quê*. Docstring curta no topo de cada módulo e em cada classe pública.
- **Erros:** não engolir exceção sem log. Adaptadores traduzem exceções da biblioteca para o resultado que a porta promete (ex.: `Publicador.publicar` devolve `False` em vez de propagar erro de rede).
- **Logs:** `logging` da biblioteca padrão, um `logger = logging.getLogger(__name__)` por módulo. Nada de `print` no código do produto.
- **SOLID aplicado:** SRP (cada módulo uma razão para mudar), OCP e DIP (casos de uso dependem de portas, modelos novos entram como adaptadores). LSP e ISP ficam garantidos por portas pequenas.
- **Ferramentas:** `ruff` (lint + formatação, linha de 100 colunas) e `pytest`, configurados em `pyproject.toml`.

## 7. Testes

- Domínio e casos de uso têm teste unitário com fakes. Não dependem de câmera, modelo, rede nem do Raspberry Pi.
- Adaptadores que usam só a biblioteca padrão (ex.: fila SQLite) têm teste real com arquivo temporário.
- Adaptadores que dependem de hardware ou modelo (câmera, DeepFace, MQTT) são testados manualmente ou em testes marcados que podem ser pulados quando a biblioteca não estiver instalada.
- Nenhum teste usa dados de alunos (RC-01): só datasets públicos (LFW, AT&T) ou dados sintéticos.

## 8. Código de pesquisa

Scripts de benchmark e preparação de dataset são experimentos. Eles não usam portas e adaptadores: cada um é um script único, com parâmetros por CLI e documentação de instalação e uso no cabeçalho. Mesmo assim, seguem todos os padrões de código da seção 6:

- type hints, dataclasses para os dados, constantes nomeadas em vez de números mágicos, `pathlib` para caminhos;
- `logging` em vez de `print`, e nenhuma exceção engolida sem log;
- bibliotecas pesadas (DeepFace, pandas, numpy, scikit-learn) importadas dentro das funções que as usam;
- lógica pura (montagem de pares, cálculo de métricas) separada da chamada ao modelo e testada em `tests/test_pesquisa.py`;
- **reprodutibilidade:** a ordem das chamadas a `random` não pode mudar, senão a mesma semente passa a gerar pares diferentes e os resultados publicados deixam de ser reproduzíveis. Qualquer refatoração deve comparar os pares gerados antes e depois.

As dependências ficam no extra `pesquisa` do `pyproject.toml`. Quando uma ideia de pesquisa virar parte do produto, ela é reescrita como adaptador em `src/presenca/adaptadores/`.

## 9. Pendências conhecidas para o TCC2

Limitações do esqueleto atual, identificadas em revisão de código em 2026-10-11. Ficaram para o TCC2 porque dependem do hardware final ou de testes reais no ônibus; corrigir agora seria chutar parâmetros ou refazer código provisório.

| Pendência | Risco | Caminho previsto |
|---|---|---|
| A sincronização roda na mesma thread que a câmera | Em rede 4G lenta, cada envio espera até `mqtt.timeout_s`; um lote de 50 eventos pode parar o reconhecimento por minutos e alunos deixam de ser registrados (RNF-02) | Sincronização em thread própria, com uma conexão SQLite por thread e o banco em modo WAL; ou envio assíncrono confirmado pelo callback do MQTT. Decidir depois de medir no Raspberry Pi 5 + Hailo |
| Alerta de baixa confiança sai no primeiro quadro ruim | Enquanto o aluno se aproxima da câmera, os primeiros quadros têm confiança baixa: quase todo embarque geraria também um alerta falso (RF-12) | Janela de confirmação: o alerta só sai se o aluno não for reconhecido com boa confiança em N segundos; rosto desconhecido só alerta se aparecer em vários quadros. Calibrar N e o número de quadros com testes no ônibus |
| Filtro `face_confidence > 0` no `ReconhecedorDeepFace` | Se o detector devolver confiança 0 para um rosto real, ele é descartado; uma foto de referência pode sumir da galeria sem aviso | O adaptador DeepFace é provisório: a comparação de detectores favoreceu o RetinaFace e a versão embarcada usará TFLite/Hailo. Tratar no adaptador definitivo, identificando "nenhum rosto" pela área detectada |

## 10. Referências

- COCKBURN, A. *Hexagonal Architecture* (Ports and Adapters), 2005.
- MARTIN, R. C. *Clean Architecture*. Prentice Hall, 2017.
- MARTIN, R. C. *Clean Code*. Prentice Hall, 2008.
- RICHARDSON, C. *Microservices Patterns*, padrão *Transactional Outbox*. Manning, 2018.
