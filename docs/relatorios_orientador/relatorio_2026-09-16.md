# Relatório de Progresso — TCC Sistema IoT para Monitoramento de Presença em Transporte Escolar Rural

**Data:** 16/09/2026
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García — **Coorientador:** Frederico Gualberto Ferreira Coelho
**Período coberto:** início do projeto (primeiro relatório)

## Resumo executivo

O cronograma detalhado (`Cronograma_Oficial.md`) foi formalizado e, desde então, houve
trabalho concentrado nas Atividades 1.1 e 1.2: o levantamento de requisitos foi
concluído (com 6 pontos em aberto explícitos), os 10 algoritmos de reconhecimento
facial candidatos foram levantados, testados empiricamente contra um dataset público
(LFW) e todos concluídos com sucesso — incluindo Dlib e o modelo "DeepFace" (Facebook),
que exigiram contorno técnico adicional. A redação da monografia também começou, com a
Introdução completa e parte da Revisão Bibliográfica (métodos clássicos pré-deep
learning, devidamente citados). As três tarefas com prazo 30/09/2026 estão concluídas
antes do previsto. A escolha dos "2 melhores" algoritmos, porém, segue preliminar: com
o resultado do Dlib incluído, o ranking muda (Dlib superou os dois modelos "leves" hoje
recomendados) e o benchmark ainda usa um detector de rosto considerado fraco para parte
dos modelos — os dois pontos precisam ser resolvidos antes de fechar a escolha. Há
também 5 questões em aberto que dependem de decisão do orientador ou de terceiros
(TRANSCOLAR RURAL).

## Progresso — atividades práticas

| Data prevista | Atividade | Status | Evidência |
|---|---|---|---|
| 30/09/2026 | Buscar os 10 melhores algoritmos para reconhecimento facial | Concluída | [resumo_reconhecimento_facial_tcc.md](../estudo_reconhecimento_facial.md), [Revisao_Bibliografica_Anotacoes.md](../revisao_bibliografica.md) |
| 30/09/2026 | Entender/implementar como usar os algoritmos escolhidos | Concluída | [benchmark_face_recognition.py](../../pesquisa/benchmark_reconhecimento_facial.py) — implementa os 10 modelos via `DeepFace.verify()`; todos os 10 executados com sucesso, incluindo Dlib (compilado localmente) e DeepFace/Facebook (via ambiente Python 3.10 dedicado) |
| 30/09/2026 | Pegar uma base de dados para teste | Concluída | [preparar_dataset.py](../../pesquisa/preparar_dataset.py); pastas `dataset/` (LFW, 96 pessoas) e `dataset_teste/` (AT&T/Olivetti) já baixadas |
| 31/10/2026 | Conseguir testar com os dados iniciais a fim de escolher o algoritmo | Adiantada | [relatorio_benchmark_reconhecimento_facial.md](../benchmark_reconhecimento_facial.md), [benchmark_resultados.csv](../../pesquisa/resultados/benchmark_resultados.csv), [benchmark_resultados.png](../../pesquisa/resultados/benchmark_resultados.png) — 10/10 modelos com resultado, tempo de inferência medido com isolamento de processo (corrige uma distorção identificada na primeira rodada) |
| 31/10/2026 | Escolher os 2 melhores de 10 | Adiantada, escolha ainda preliminar | Recomendação atual (ArcFace + SFace, segundo o relatório de benchmark) foi definida **antes** de trocar o detector de rosto por um mais robusto — ver Pendências |
| 31/10/2026 | Aumentar a base de dados para realmente testar os escolhidos | Não iniciada | — |
| 30/11/2026 | Ver como emular o ambiente do Raspberry Pi AI HAT (Hailo-10) no computador | Não iniciada | — |

## Progresso — entregas de documentação

| Data prevista | Entrega | Status | Evidência |
|---|---|---|---|
| 11/10/2026 | Entrega do documento de Visão Geral | Não iniciada | Será um documento separado de `requisitos.md` (decisão confirmada — ver Decisões tomadas); `requisitos.md` segue como levantamento de requisitos da Atividade 1.1, com 6 pontos em aberto (seção 5) |
| 13/11/2026 | Entrega do Texto Inicial da Monografia | Em andamento | [monografia_tcc1.tex](../../monografia/monografia_tcc1.tex) — estrutura em abnTeX2 criada; capítulo de Introdução completo; Revisão Bibliográfica parcialmente escrita (métodos clássicos — Eigenfaces, Fisherfaces, LBPH — citados via `referencias.bib`), ainda falta a comparação empírica dos 10 algoritmos, reconhecimento de voz e protocolos MQTT; Metodologia, Avaliação de Impactos e Cronograma do TCC II ainda não escritos |
| 16/11 a 19/11/2026 | Seminários de TCC I | Não iniciada (fora do horizonte atual) | — |

## Decisões tomadas

- **Não persistir imagem/áudio bruto dos alunos** — o sistema deve armazenar apenas o
  resultado do processamento (evento de presença). Confirmado com a aluna e registrado
  como RF-05/RNF-07 em `requisitos.md`.
- **Fixar `opencv-python==4.10.0.84`** — a versão mais recente (5.0.0) não inclui os
  arquivos de cascata Haar necessários, quebrando o detector `opencv` silenciosamente.
- **Detector de rosto do benchmark: OpenCV (Haar Cascade)** — escolhido por ser o mais
  leve; ainda não foi substituído por um detector mais robusto (ver Pendências).
- **Correção de metodologia de medição de tempo**: cada modelo do benchmark passou a
  rodar em processo isolado (`multiprocessing`), porque o DeepFace mantém modelos
  carregados em memória e distorcia o tempo dos modelos avaliados por último — um dos
  achados apontou o SFace como 47x mais lento do que realmente é antes da correção.
- **Dois ambientes virtuais Python** — `.venv/` (Python 3.13, TensorFlow 2.21) para 9
  dos 10 modelos, e `.venv_deepface_legacy/` (Python 3.10, TensorFlow ≤2.12) só para o
  modelo "DeepFace" (Facebook), que depende de uma camada do Keras removida em versões
  mais novas do TensorFlow.
- **Dlib compilado localmente** (CMake + Visual Studio Build Tools/MSVC), já que não há
  wheel pré-compilada para Python 3.13 no Windows — isso limita a reprodutibilidade em
  outra máquina sem o mesmo toolchain de compilação.
- **Estrutura da monografia definida em abnTeX2**, com cinco capítulos (Introdução,
  Revisão Bibliográfica, Metodologia, Avaliação de Impactos Socioeconômicos/Legais/de
  Humanidades, Cronograma do TCC II).
- **Eigenfaces, Fisherfaces e LBPH citados na Revisão Bibliográfica como marco
  histórico, mas deliberadamente fora da comparação empírica** — por não estarem
  disponíveis na biblioteca DeepFace (exigiriam pipeline de pré-processamento à parte)
  e por serem, segundo a literatura, muito sensíveis a condições de iluminação/ângulo
  não controladas, como as esperadas dentro de um ônibus escolar em movimento.
- **Datasets usados são só de adultos que consentiram em pesquisa pública** (LFW,
  AT&T/Olivetti) — nenhum dado real de aluno é usado nesta fase, por restrição de LGPD
  ainda não formalizada (Atividade 1.4).
- **O documento de "Visão Geral" (entrega de 11/10) será separado de `requisitos.md`** —
  este último cobre o levantamento de requisitos da Atividade 1.1, mas não substitui a
  entrega formal de Visão Geral.

## Pendências e próximos passos

1. **Repetir o benchmark com um detector de rosto mais robusto** (`retinaface` ou
   `yunet` em vez de `opencv`) — o detector atual é suspeito de gerar recall
   artificialmente baixo em alguns modelos (Facenet, Facenet512, SFace), o que pode
   mudar a leitura final antes de fechar a escolha dos 2 algoritmos.
2. **Reavaliar a escolha dos "2 melhores" considerando o Dlib**, que ficou em 3º lugar
   em acurácia (84,90%) — acima dos modelos "leves" hoje recomendados como opção de
   baixo custo — mas exige compilação manual, o que pesa contra ele em reprodutibilidade.
3. Escrever os capítulos restantes da monografia (o restante da Revisão Bibliográfica —
   comparação empírica dos 10 algoritmos, reconhecimento de voz, MQTT —, Metodologia,
   Avaliação de Impactos e Cronograma do TCC II) e, por último, o Resumo/Abstract.
4. Popular `referencias.bib` com as fontes dos 10 algoritmos de aprendizado profundo à
   medida que a comparação empírica for redigida na Revisão Bibliográfica.
5. Aumentar a base de dados de teste para os algoritmos finalmente escolhidos.
6. Investigar a emulação do ambiente Raspberry Pi AI HAT / Hailo-10.
7. Iniciar o documento de Visão Geral (separado de `requisitos.md`), com entrega prevista para 11/10/2026.
8. Resolver as 5 questões em aberto listadas abaixo.

## Pontos que precisam de decisão ou orientação

1. **Especificação técnica do TRANSCOLAR RURAL** — não há, nos materiais do projeto,
   documentação sobre a API/protocolo desse sistema externo, necessária para detalhar
   os requisitos de integração (RF-06 a RF-08). Há um contato técnico que possa
   fornecer essa especificação? Ou essa parte será mockada?
2. **Latência máxima tolerada no embarque/desembarque (RNF-02)** — a proposta prevê que
   esse valor seria "mapeado" na Atividade 1.1, mas nenhum número foi definido. Há uma
   referência de tempo médio de embarque que ajude a estimar um valor razoável (ex.:
   <2s, <5s)?
3. **Papel do motorista/monitor do ônibus** — ficou definido que não terá "perfil de
   usuário" no sistema, mas fisicamente alguém opera o embarque. O dispositivo precisa
   de algum feedback local (luz/som) confirmando o reconhecimento, mesmo sem tela/login?
4. **Retenção dos eventos de presença** — por quanto tempo os dados derivados (ex.:
   "aluno X embarcou às 7h14") devem ficar armazenados, no dispositivo e no TRANSCOLAR
   RURAL?
5. **Fluxo de consentimento dos responsáveis** para o cadastro biométrico de referência
   (RF-18) — faz parte do escopo deste sistema (ex.: tela de opt-in) ou é um processo
   administrativo da escola, fora do sistema?
