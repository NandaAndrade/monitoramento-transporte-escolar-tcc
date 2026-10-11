# Relatório de Progresso — TCC Sistema IoT para Monitoramento de Presença em Transporte Escolar Rural

**Data:** 11/10/2026
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García — **Coorientador:** Frederico Gualberto Ferreira Coelho
**Período coberto:** desde o último relatório, em 16/09/2026

## Resumo executivo

O benchmark de reconhecimento facial foi repetido com o detector RetinaFace. O ArcFace se
manteve como o melhor modelo (96,61% de acurácia). O segundo modelo continua em aberto:
o SFace não melhorou e o VGG-Face passou de 90%. O documento de Visão Geral foi escrito
(`monografia/visao_geral.tex`) e sua entrega foi adiada de 11/10 para 18/10/2026. Ainda
faltam os resultados do RetinaFace e alguns pontos marcados como pendentes. Quatro das
cinco questões abertas no relatório anterior foram respondidas nos requisitos (ver
Decisões tomadas). Também foi adiantado o esqueleto do software embarcado. Em
compensação, o texto da monografia não avançou no período, e as Atividades 1.3
(diagramas UML e banco de dados) e 1.4 (impactos), previstas para outubro, ainda não
começaram.

## Progresso — atividades práticas

| Data prevista | Atividade | Status | Evidência |
|---|---|---|---|
| 30/09/2026 | Buscar os 10 melhores algoritmos para reconhecimento facial | Concluída | [estudo_reconhecimento_facial.md](../estudo_reconhecimento_facial.md), [revisao_bibliografica.md](../revisao_bibliografica.md) |
| 30/09/2026 | Entender/implementar como usar os algoritmos escolhidos | Concluída | [benchmark_reconhecimento_facial.py](../../pesquisa/benchmark_reconhecimento_facial.py) |
| 30/09/2026 | Pegar uma base de dados para teste | Concluída | [preparar_dataset.py](../../pesquisa/preparar_dataset.py); `pesquisa/dados/lfw/` e `pesquisa/dados/att/` |
| 31/10/2026 | Conseguir testar com os dados iniciais a fim de escolher o algoritmo | Em andamento (no prazo) | [benchmark_reconhecimento_facial.md](../benchmark_reconhecimento_facial.md), seção 7: os 10 modelos foram avaliados com os detectores OpenCV e RetinaFace ([comparar_detectores.py](../../pesquisa/comparar_detectores.py), [benchmark_comparacao_detectores.csv](../../pesquisa/resultados/benchmark_comparacao_detectores.csv)); falta a rodada com o YuNet |
| 31/10/2026 | Escolher os 2 melhores de 10 | Em andamento (no prazo) | ArcFace confirmado em 1º lugar; o 2º está entre SFace (leve, 79,69%) e VGG-Face (95,57%, 580 MB) |
| 31/10/2026 | Aumentar a base de dados para realmente testar os escolhidos | Não iniciada (20 dias para o prazo) | Depende da escolha dos 2 modelos |
| 30/11/2026 | Ver como emular o ambiente do Raspberry Pi AI HAT (Hailo-10) Kit no computador e se precisa trocar a linguagem | Não iniciada (no prazo) | — |

## Progresso — entregas de documentação

| Data prevista | Entrega | Status | Evidência |
|---|---|---|---|
| 18/10/2026 (adiada de 11/10/2026) | Entrega do documento de Visão Geral | Em andamento | [visao_geral.tex](../../monografia/visao_geral.tex): texto completo no modelo oficial do curso, com 10 marcações `\pendente{}` (resultados do RetinaFace, especificação do TRANSCOLAR RURAL, referências de voz e de trabalhos correlatos, meses do TCC II) |
| 13/11/2026 | Entrega do Texto Inicial da Monografia | Em andamento, sem avanço no texto no período | [monografia_tcc1.tex](../../monografia/monografia_tcc1.tex) continua igual ao do último relatório: Introdução completa e Revisão Bibliográfica parcial. [referencias.bib](../../monografia/referencias.bib) passou de 3 para 13 referências (ArcFace, SFace, FaceNet, RetinaFace, YuNet, LFW, AT&T, DeepFace/LightFace, MQTT, LGPD). Faltam Metodologia, Avaliação de Impactos, Cronograma do TCC II, a comparação empírica, voz e MQTT |
| 16/11/2026 a 19/11/2026 | Seminários de TCC I | Não iniciada (no prazo) | — |

## Ressalvas técnicas

- **O tempo do detector pesa tanto quanto o do reconhecedor.** Na CPU do PC, o RetinaFace
  leva cerca de 0,62 s por imagem e deixa o ArcFace em 1,80 s por par, perto do limite de
  2 s do RNF-02. No Raspberry Pi, a detecção também vai precisar rodar no Hailo ou usar um
  detector leve. Por isso, a escolha do detector precisa fazer parte da decisão da
  Atividade 1.2.
- **O limiar de decisão não foi calibrado.** Todos os modelos usam o limiar padrão do
  DeepFace. Isso explica o padrão "precisão ≈ 100% e recall baixo" no SFace, no
  GhostFaceNet e no Dlib, que não melhoraram com o RetinaFace. Como o critério do projeto
  passou a priorizar a precisão (ver Decisões tomadas), a acurácia com o limiar padrão
  não é a métrica certa para escolher. A comparação deveria fixar uma meta de precisão
  (ou de taxa de falsos positivos) e, para cada modelo, ajustar o limiar e medir o recall
  obtido nesse ponto, em um conjunto separado.
- **A diferença entre o 1º e o 2º lugar está dentro da margem de erro.** Com 384 pares, o
  intervalo de confiança de 95% para uma acurácia de cerca de 96% é de aproximadamente
  ±2 pontos percentuais. Assim, ArcFace (96,61%) e VGG-Face (95,57%) não se distinguem
  estatisticamente nessa amostra. Ampliar a base é necessário para confirmar a escolha,
  e não apenas uma formalidade.
- **A tarefa testada não é a tarefa do sistema.** O benchmark mede verificação 1:1 com
  fotos de adultos (LFW). O sistema fará identificação 1:N entre cerca de 20 crianças,
  com a iluminação e o ângulo da porta do ônibus. Essa diferença precisa aparecer como
  limitação na monografia e orientar a ampliação da base de dados.
- **A implementação foi adiantada enquanto atividades do TCC I estão paradas.** O
  esqueleto do software embarcado (`src/presenca/`) é escopo do TCC II e avançou enquanto
  as Atividades 1.3 e 1.4 e os capítulos da monografia não começaram. O esqueleto ajuda
  a concretizar a arquitetura da Atividade 1.3, mas não substitui os diagramas UML e a
  modelagem de banco previstos.

## Decisões tomadas

- **Requisitos que estavam em aberto** ([requisitos.md](../requisitos.md), seção 5.1):
  - latência máxima de 2 s por aluno, da detecção ao retorno local (RNF-02), a revalidar
    no hardware embarcado;
  - o motorista ou monitor não tem perfil de usuário, mas o dispositivo dá retorno local
    por LED e bipe, de confirmação ou de falha (RF-20);
  - os eventos ficam no dispositivo só até o envio ser confirmado; no backend, ficam
    durante o ano letivo corrente mais 1 ano e depois são eliminados ou anonimizados
    (RNF-16);
  - o consentimento dos responsáveis é coletado pela escola, fora do sistema; o sistema
    registra o consentimento, bloqueia o cadastro biométrico sem ele e trata a revogação
    (RF-18, RF-21).
- **Critério de erro: registrar o aluno errado (falso positivo) é pior do que deixar de
  registrar um aluno (falso negativo).** O limiar de cada modelo será calibrado priorizando
  a precisão, mesmo à custa de recall. Um aluno não reconhecido ainda pode ser tratado pelo
  retorno local de falha (LED e bipe); um registro errado gera uma informação falsa para a
  escola e para os responsáveis. Registrado em RNF-03 de [requisitos.md](../requisitos.md).
- **O reconhecimento de voz fica para o TCC II.** No TCC I, a voz entra apenas na revisão
  bibliográfica; a seleção e a avaliação do modelo de reconhecimento de locutor serão
  feitas no TCC II. Registrado em [requisitos.md](../requisitos.md) e no documento de
  Visão Geral.
- **Tendência de hardware: Raspberry Pi 5 com AI HAT (Hailo-10) em vez de ESP32.** O ESP32
  não tem capacidade para rodar com folga os modelos pré-selecionados dentro do limite de
  2 s. A decisão formal fica para a Atividade 1.3.
- **Benchmark com cache de detecção.** Cada imagem é detectada e alinhada uma única vez, e
  os 10 modelos rodam sobre os mesmos recortes. Assim, a comparação entre detectores fica
  justa e o tempo de detecção é medido separado do tempo de reconhecimento.
- **Arquitetura do software embarcado** ([arquitetura.md](../arquitetura.md)):
  - arquitetura hexagonal (portas e adaptadores), para trocar modelo, câmera ou meio de
    envio sem mexer na regra de negócio (RNF-14);
  - fila local em SQLite com MQTT QoS 1 e UUID por evento (store-and-forward), para não
    perder nem duplicar presenças com rede instável (RF-07, RF-08);
  - nenhuma imagem é gravada em disco, log ou rede (LGPD).
- **O repositório passou a usar git e foi reorganizado** em `docs/`, `monografia/`,
  `pesquisa/` e `src/`, para ter histórico confiável do trabalho.

## Pendências e próximos passos

1. Finalizar a Visão Geral até 18/10: atualizar a tabela e a escolha com os resultados do
   RetinaFace e resolver as marcações `\pendente{}`.
2. Rodar o benchmark com o detector YuNet e calibrar o limiar de cada modelo priorizando a
   precisão (ver Ressalvas técnicas) antes de fechar os 2 modelos, até 31/10.
3. Ampliar a base de dados de teste para os 2 modelos escolhidos (até 31/10).
4. Atividade 1.3: diagramas UML, modelagem do banco de dados (PostgreSQL ou Firebase) e
   decisão formal de hardware.
5. Atividade 1.4: análise de impactos socioeconômicos, ambientais e de privacidade.
6. Escrever os capítulos que faltam na monografia até 13/11 e completar o `referencias.bib`
   com os modelos que ainda faltam (VGG-Face, Dlib, GhostFaceNet, DeepFace, DeepID,
   OpenFace) e com as referências de voz para a revisão bibliográfica.
7. Estudar a emulação do Hailo-10 no computador (até 30/11), verificando também quais dos
   modelos candidatos têm versão compilável para o acelerador.

## Pontos que precisam de decisão ou orientação

1. **Especificação técnica do TRANSCOLAR RURAL**, que continua pendente desde o último
   relatório. Há um contato que possa fornecer a API ou o formato das mensagens? Se não
   houver, a integração pode ser simulada (mock) no TCC?
2. **Confirmação das quatro decisões de requisitos** listadas em Decisões tomadas
   (latência de 2 s, LED e bipe, retenção, consentimento). Elas atendem ao que o
   orientador esperava?
