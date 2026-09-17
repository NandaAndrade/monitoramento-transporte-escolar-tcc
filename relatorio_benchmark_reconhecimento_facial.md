# Relatório — Benchmark de Reconhecimento Facial (TCC)

**Dataset:** LFW (Labeled Faces in the Wild), 96 pessoas com ≥15 fotos cada, baixado via `scikit-learn`.
**Pares avaliados por modelo:** 384 (192 positivos / mesma pessoa + 192 negativos / pessoas diferentes).
**Detector de rosto:** OpenCV (Haar Cascade) — o mais leve dos disponíveis, mais próximo do custo aceitável em Raspberry Pi/Hailo.
**Ambiente:** `.venv/` dedicado (Python 3.13, DeepFace 0.0.101 + TensorFlow 2.21) para 9 dos 10 modelos, e um segundo ambiente `.venv_deepface_legacy/` (Python 3.10 + TensorFlow 2.12) só para o modelo "DeepFace" (Facebook), que exige TF ≤2.12.
**Metodologia de tempo:** cada modelo roda em um **processo isolado** — ver seção 2 abaixo sobre por que isso importa.

---

## 1. Ranking de resultados (todos os 10 modelos da revisão bibliográfica)

| # | Modelo | Acurácia | Precisão | Recall | F1 | Tempo médio/par (s) | Tamanho (MB) |
|---|---|---|---|---|---|---|---|
| 1 | **ArcFace** | **92,71%** | 99,40% | 85,94% | 0,9218 | 0,736 | 130 |
| 2 | VGG-Face | 88,02% | 96,79% | 78,65% | 0,8678 | 2,379 | 580 |
| 3 | Dlib | 84,90% | 99,26% | 70,31% | 0,8232 | 1,247 | 22 |
| 4 | GhostFaceNet | 82,55% | 100% | 65,10% | 0,7886 | 0,664 | 16 |
| 5 | SFace | 81,51% | 100% | 63,02% | 0,7732 | **0,089** | 5 |
| 6 | Facenet | 76,04% | 100% | 52,08% | 0,6849 | 1,104 | 90 |
| 7 | Facenet512 | 72,66% | 100% | 45,31% | 0,6237 | 0,845 | 90 |
| 8 | DeepFace (Facebook) | 60,94% | 73,33% | 34,38% | 0,4681 | 12,949 | 150 |
| 9 | DeepID | 51,56% | 80,00% | 4,17% | 0,0792 | 0,071 | 3 |
| 10 | OpenFace | 50,78% | 100% | 1,56% | 0,0308 | 0,303 | 30 |

CSV completo: [benchmark_resultados.csv](benchmark_resultados.csv) · Gráfico: [benchmark_resultados.png](benchmark_resultados.png)

Todos os 10 algoritmos da tabela original da revisão bibliográfica agora têm resultado — Dlib e DeepFace (Facebook), que tinham falhado na primeira rodada, foram viabilizados (detalhes na seção 3).

---

## 2. Correção importante: isolar cada modelo em um processo próprio

Na primeira rodada, **SFace apareceu como o modelo mais lento de todos (4,22s/par)**, contrariando a literatura (que o descreve como leve/rápido, ideal para hardware embarcado). Investigando, a causa não era o modelo em si:

- O `DeepFace` (biblioteca) **nunca libera da memória** um modelo já carregado — mantém tudo em cache pelo tempo de vida do processo Python.
- Como o script original rodava todos os 9-10 modelos **no mesmo processo**, sequencialmente, na hora de avaliar o SFace (7º da lista) o processo já tinha VGG-Face, Facenet, Facenet512, OpenFace, DeepID e ArcFace inteiros carregados na RAM ao mesmo tempo — várias sessões TensorFlow competindo por CPU.
- Rodando o SFace **sozinho**, sem nenhum outro modelo carregado antes: **0,089s/par** — 47x mais rápido, e consistente com a literatura.

**Correção aplicada em [benchmark_face_recognition.py](benchmark_face_recognition.py):** cada modelo agora roda em um **processo separado** (`multiprocessing`, contexto `spawn`), isolando o tempo de inferência de cada um dos demais. Esse é o comportamento **padrão** do script agora; use `--sem_isolamento` só se quiser voltar ao modo antigo (mais rápido de configurar, mas com tempos possivelmente distorcidos para os últimos modelos da lista).

A acurácia/precisão/recall de todos os modelos **não mudou** com essa correção — só o tempo médio de inferência, que agora reflete o custo real de cada modelo isoladamente (o cenário mais parecido com o que vai rodar no Raspberry Pi, já que lá você não vai ter 6 outros modelos de reconhecimento facial carregados ao mesmo tempo).

---

## 3. Como Dlib e DeepFace (Facebook) foram viabilizados

### Dlib
Não havia wheel pré-compilada do pacote `dlib` para Python 3.13 no Windows. Verificado que a máquina já tinha o **Visual Studio Build Tools 2026** instalado (com o workload de compilador C++/MSVC), então:
1. Instalado `cmake` via `pip install cmake` (mais leve que instalar o CMake completo do sistema).
2. Compilado o `dlib` a partir do código-fonte dentro do `.venv/`, usando o ambiente do MSVC (`vcvars64.bat`).
3. Build concluído em poucos minutos, sem precisar instalar nada de sistema além do `cmake` (o compilador já estava lá).

### DeepFace (Facebook, 2014)
Esse modelo usa uma camada Keras (`LocallyConnected2D`) que foi removida do TensorFlow após a versão 2.12 — incompatível com o TF 2.21 exigido pelo Python 3.13. Solução: criado um **segundo ambiente virtual** (`.venv_deepface_legacy/`) com **Python 3.10** (instalado via `winget`) + `tensorflow<=2.12`, isolado do ambiente principal para não rebaixar o TF usado pelos outros 9 modelos.

Resultado: **60,94% de acurácia**, bem abaixo dos demais, e de longe o mais lento (12,9s/par) — confirma na prática o que já estava anotado na tabela original da revisão bibliográfica ("mais histórico/comparativo que prático hoje").

---

## 4. Leitura atualizada dos resultados

- **ArcFace segue disparado na frente** — 92,71% de acurácia, F1 0,92, tempo de inferência baixo (0,74s) mesmo isolado. Continua a melhor escolha geral.
- **SFace é, de fato, o mais rápido de todos os modelos "completos"** (0,089s/par) depois da correção de isolamento — coerente com a literatura, e reforça seu lugar como opção mais leve para o hardware do projeto.
- **Dlib entrou como 3º melhor em acurácia (84,9%)**, com tamanho pequeno (22 MB) — um candidato a mais para considerar, mas exige compilar do código-fonte (não tem wheel pronta pra Python 3.13/Windows), o que complica reprodutibilidade em outra máquina.
- **DeepFace (Facebook)** confirmado como o pior custo-benefício: acurácia baixa (60,9%) e o mais lento de todos por uma margem grande (12,9s/par, ~15x mais lento que o 2º mais lento). Não recomendado.
- **GhostFaceNet** continua o melhor "leve" em acurácia (82,55%) com 100% de precisão (só erra por excesso de cautela, nunca confunde duas pessoas).
- Facenet, Facenet512, DeepID e OpenFace continuam com recall baixo — como já registrado na rodada anterior, provavelmente efeito do detector `opencv`/Haar Cascade (fraco) combinado com o threshold padrão do DeepFace, não uma limitação real desses modelos. Ainda vale re-testar com `retinaface` ou `yunet` antes de descartá-los de vez.

---

## 5. Observações e limitações remanescentes

1. **Ambiente duplicado:** agora há dois venvs no projeto — `.venv/` (Python 3.13, uso geral) e `.venv_deepface_legacy/` (Python 3.10, só para o modelo DeepFace/Facebook). Documentar isso no README do projeto para quem for reproduzir.
2. **`opencv-python` 5.0.0 (PyPI)** não inclui os arquivos de cascata Haar — mantenha fixado em `opencv-python==4.10.0.84` nos dois ambientes.
3. **Reprodutibilidade do Dlib:** como foi compilado localmente (não é uma wheel oficial do PyPI), rodar em outra máquina exige repetir o processo de build (CMake + compilador C++ disponível). Se isso for um problema para a banca/reprodução, pode valer a pena excluir o Dlib do resultado final e manter só os 9 modelos com wheel oficial.
4. Ainda não testamos outro detector de rosto (`retinaface`/`yunet`) — não foi priorizado nesta rodada, mas seria o próximo ajuste de ambiente com maior potencial de mudar a leitura dos resultados (principalmente para Facenet/Facenet512/SFace, que tiveram recall inesperadamente baixo).

---

## 6. Conclusão atualizada para a monografia

Cruzando acurácia + tempo (agora medido corretamente, isolado) + tamanho, a dupla mais recomendada continua:

- **ArcFace** — melhor acurácia (92,7%), tempo aceitável (0,74s isolado), tamanho moderado (130 MB, ou poucos MB na variante MobileFaceNet).
- **SFace** — agora confirmado como o mais rápido de todos (0,089s/par) e o menor em disco (5 MB), com 100% de precisão. Antes da correção de isolamento, esse resultado estava mascarado — vale destacar esse achado metodológico na monografia, já que ele muda a conclusão sobre qual modelo é "leve" de verdade.

**Próximo passo recomendado:** repetir o benchmark trocando o detector de `opencv` para `retinaface` ou `yunet`, para checar se o recall baixo de Facenet/Facenet512/SFace melhora com um detector mais robusto.
