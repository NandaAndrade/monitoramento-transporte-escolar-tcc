# Relatório de Progresso — TCC Sistema IoT para Monitoramento de Presença em Transporte Escolar Rural

**Data:** 16/09/2026
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García — **Coorientador:** Frederico Gualberto Ferreira Coelho
**Período coberto:** início do projeto (primeiro relatório)

## Resumo executivo

O cronograma detalhado (`Cronograma_Oficial.md`) foi formalizado e, desde então, houve trabalho concentrado nas Atividades 1.1 e 1.2: o levantamento de requisitos foi concluído (com pontos em aberto explícitos), os 10 algoritmos de reconhecimento facial candidatos foram levantados e testados empiricamente contra um dataset público (LFW), e a redação da monografia foi iniciada, com o capítulo de Introdução já escrito. As três tarefas com prazo 30/09/2026 estão concluídas antes do previsto, e as de 31/10/2026 estão parcialmente adiantadas. A escolha dos "2 melhores" algoritmos ainda é preliminar e depende de duas pendências técnicas detalhadas abaixo. Há também 7 questões em aberto que dependem de decisão do orientador ou de terceiros (TRANSCOLAR RURAL).

## Progresso — atividades práticas

| Data prevista | Atividade | Status | Evidência |
|---|---|---|---|
| 30/09/2026 | Buscar os 10 melhores algoritmos para reconhecimento facial | Concluída | [resumo_reconhecimento_facial_tcc.md](../resumo_reconhecimento_facial_tcc.md), [Revisao_Bibliografica_Anotacoes.md](../Revisao_Bibliografica_Anotacoes.md) |
| 30/09/2026 | Entender/implementar como usar os algoritmos escolhidos | Concluída | [benchmark_face_recognition.py](../benchmark_face_recognition.py) — implementa os 10 modelos via `DeepFace.verify()`; todos executados com sucesso, incluindo o Dlib |
| 30/09/2026 | Pegar uma base de dados para teste | Concluída | [preparar_dataset.py](../preparar_dataset.py); pastas `dataset/` (LFW, 96 pessoas) e `dataset_teste/` (AT&T/Olivetti) já baixadas |
| 31/10/2026 | Conseguir testar com os dados iniciais a fim de escolher o algoritmo | Adiantada | [benchmark_resultados.csv](../benchmark_resultados.csv), [benchmark_resultados.png](../benchmark_resultados.png), [_dlib_resultados.csv](../_dlib_resultados.csv) |
| 31/10/2026 | Escolher os 2 melhores de 10 | Adiantada, escolha preliminar | [relatorio_benchmark_reconhecimento_facial.md](../relatorio_benchmark_reconhecimento_facial.md) aponta ArcFace e GhostFaceNet — ver Ressalvas técnicas |
| 31/10/2026 | Aumentar a base de dados para realmente testar os escolhidos | Não iniciada | — |
| 30/11/2026 | Ver como emular o ambiente do Raspberry Pi AI HAT (Hailo-10) no computador | Não iniciada | — |

## Progresso — entregas de documentação

| Data prevista | Entrega | Status | Evidência |
|---|---|---|---|
| 11/10/2026 | Entrega do documento de Visão Geral | Em andamento | [requisitos.md](../requisitos.md) — requisitos funcionais/não funcionais, restrições e rastreabilidade com a proposta; 6 pontos em aberto (seção 5) |
| 13/11/2026 | Entrega do Texto Inicial da Monografia | Em andamento | [monografia_tcc1.tex](../monografia_tcc1.tex) — estrutura em abnTeX2 criada, capítulo de Introdução redigido; Revisão Bibliográfica, Metodologia, Avaliação de Impactos e Cronograma do TCC II ainda são placeholders |
| 16/11 a 19/11/2026 | Seminários de TCC I | Não iniciada (fora do horizonte atual) | — |

## Ressalvas técnicas

- **Documento de interpretação do benchmark desatualizado.** `relatorio_benchmark_reconhecimento_facial.md` ainda reflete a rodada anterior de testes: não menciona o Dlib (testado com sucesso depois, 84,90% de acurácia) nem os tempos de inferência da rodada mais recente.
- **Ranking muda com o Dlib incluído.** Por acurácia: ArcFace (92,71%) > VGG-Face (88,02%) > Dlib (84,90%) > GhostFaceNet (82,55%) > SFace (81,51%). O Dlib superou os dois modelos "leves" que hoje aparecem recomendados como opção de baixo custo — a recomendação de "2 melhores" ainda não foi refeita considerando esse dado.
- **Detector de rosto do benchmark ainda não foi trocado.** O relatório de benchmark original já recomendava repetir os testes com `retinaface` ou `yunet` em vez de `opencv`, por suspeita de recall artificialmente baixo em alguns modelos (Facenet, Facenet512, SFace). Essa troca ainda não foi feita.

## Decisões tomadas

- **Não persistir imagem/áudio bruto dos alunos** — o sistema deve armazenar apenas o resultado do processamento (evento de presença), não a captura bruta. Confirmado com a aluna e registrado como RF-05/RNF-07 em `requisitos.md`.
- **Detector de rosto do benchmark: OpenCV (Haar Cascade)** — escolhido por ser o mais leve, mais próximo do custo aceitável em Raspberry Pi/Hailo.
- **Fixar `opencv-python==4.10.0.84`** — a versão mais recente (5.0.0) não inclui os arquivos de cascata Haar necessários, quebrando o detector silenciosamente.
- **Ambiente de testes isolado em Python 3.13** (`.venv/`) — o Python global da máquina (3.14) ainda não é suportado pelo TensorFlow.
- **Datasets usados são só de adultos que consentiram em pesquisa pública** (LFW, AT&T/Olivetti) — nenhum dado real de aluno é usado nesta fase de prototipagem, por restrição de LGPD ainda não formalizada (Atividade 1.4).
- **Estrutura da monografia definida em abnTeX2**, com cinco capítulos (Introdução, Revisão Bibliográfica, Metodologia, Avaliação de Impactos Socioeconômicos/Legais/de Humanidades, Cronograma do TCC II) — refletindo os objetivos específicos e o escopo do TCC I definidos na proposta.
- **`referencias.bib` mantido vazio até haver citação real** — para evitar inventar referências antes de a Revisão Bibliográfica ser escrita com fontes reais.

## Pendências e próximos passos

1. Atualizar `relatorio_benchmark_reconhecimento_facial.md` com os resultados do Dlib e os novos tempos de inferência.
2. Repetir o benchmark com detector `retinaface` ou `yunet` (ver Ressalvas técnicas).
3. Reavaliar a escolha dos "2 melhores" considerando o resultado do Dlib.
4. Escrever os capítulos restantes da monografia (Revisão Bibliográfica, Metodologia, Avaliação de Impactos, Cronograma do TCC II) e, por último, o Resumo/Abstract.
5. Popular `referencias.bib` com fontes reais assim que a Revisão Bibliográfica for escrita.
6. Aumentar a base de dados para os algoritmos finalmente escolhidos.
7. Investigar a emulação do ambiente Raspberry Pi AI HAT / Hailo-10.
8. Resolver as 7 questões em aberto listadas abaixo.

## Pontos que precisam de decisão ou orientação

1. **`requisitos.md` conta como a "Entrega do documento de Visão Geral"** prevista para 11/10/2026, ou é esperado um documento separado com esse nome específico?
2. **Especificação técnica do TRANSCOLAR RURAL** — não há, nos materiais do projeto, documentação sobre a API/protocolo desse sistema externo, necessária para detalhar os requisitos de integração (RF-06 a RF-08). Há um contato técnico responsável por esse sistema que possa fornecer essa especificação?
3. **Latência máxima tolerada no embarque/desembarque (RNF-02)** — a proposta original prevê que esse valor seria "mapeado" na Atividade 1.1, mas nenhum número foi definido. Há uma referência de tempo médio de embarque que ajude a estimar um valor razoável (ex.: <2s, <5s)?
4. **Papel do motorista/monitor do ônibus** — ficou definido que não terá "perfil de usuário" no sistema, mas fisicamente alguém opera o embarque. O dispositivo precisa de algum feedback local (luz/som) confirmando o reconhecimento, mesmo sem tela/login?
5. **Retenção dos eventos de presença** — por quanto tempo os dados derivados (ex.: "aluno X embarcou às 7h14") devem ficar armazenados, tanto no dispositivo quanto no TRANSCOLAR RURAL?
6. **Fluxo de consentimento dos responsáveis** para o cadastro biométrico de referência (RF-18) — faz parte do escopo deste sistema (ex.: tela de opt-in) ou é um processo administrativo da escola, fora do sistema?
7. **A estrutura de capítulos definida para a monografia** (Introdução, Revisão Bibliográfica, Metodologia, Avaliação de Impactos, Cronograma do TCC II) está de acordo com o que é esperado para o TCC I, ou falta/sobra algum capítulo?
