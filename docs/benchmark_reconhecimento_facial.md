# Relatório — Benchmark de Reconhecimento Facial (TCC)

**Dataset:** LFW (Labeled Faces in the Wild), 96 pessoas com ≥15 fotos cada, baixado via `scikit-learn`.
**Pares avaliados por modelo:** 384 (192 positivos / mesma pessoa + 192 negativos / pessoas diferentes).
**Detector de rosto:** OpenCV (Haar Cascade) — o mais leve dos disponíveis, mais próximo do custo aceitável em Raspberry Pi/Hailo. Comparado com o RetinaFace na seção 7.
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

CSV completo: [benchmark_resultados.csv](../pesquisa/resultados/benchmark_resultados.csv) · Gráfico: [benchmark_resultados.png](../pesquisa/resultados/benchmark_resultados.png)

Todos os 10 algoritmos da tabela original da revisão bibliográfica agora têm resultado — Dlib e DeepFace (Facebook), que tinham falhado na primeira rodada, foram viabilizados (detalhes na seção 3).

---

## 2. Correção importante: isolar cada modelo em um processo próprio

Na primeira rodada, **SFace apareceu como o modelo mais lento de todos (4,22s/par)**, contrariando a literatura (que o descreve como leve/rápido, ideal para hardware embarcado). Investigando, a causa não era o modelo em si:

- O `DeepFace` (biblioteca) **nunca libera da memória** um modelo já carregado — mantém tudo em cache pelo tempo de vida do processo Python.
- Como o script original rodava todos os 9-10 modelos **no mesmo processo**, sequencialmente, na hora de avaliar o SFace (7º da lista) o processo já tinha VGG-Face, Facenet, Facenet512, OpenFace, DeepID e ArcFace inteiros carregados na RAM ao mesmo tempo — várias sessões TensorFlow competindo por CPU.
- Rodando o SFace **sozinho**, sem nenhum outro modelo carregado antes: **0,089s/par** — 47x mais rápido, e consistente com a literatura.

**Correção aplicada em [benchmark_reconhecimento_facial.py](../pesquisa/benchmark_reconhecimento_facial.py):** cada modelo agora roda em um **processo separado** (`multiprocessing`, contexto `spawn`), isolando o tempo de inferência de cada um dos demais. Esse é o comportamento **padrão** do script agora; use `--sem_isolamento` só se quiser voltar ao modo antigo (mais rápido de configurar, mas com tempos possivelmente distorcidos para os últimos modelos da lista).

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
- Facenet, Facenet512, DeepID e OpenFace continuam com recall baixo — como já registrado na rodada anterior, provavelmente efeito do detector `opencv`/Haar Cascade (fraco) combinado com o threshold padrão do DeepFace, não uma limitação real desses modelos. *(Re-testado com `retinaface` na seção 7: o detector explica só parte disso — Facenet e Facenet512 melhoraram, DeepID e OpenFace não.)*

---

## 5. Observações e limitações remanescentes

1. **Ambiente duplicado:** agora há dois venvs no projeto — `.venv/` (Python 3.13, uso geral) e `.venv_deepface_legacy/` (Python 3.10, só para o modelo DeepFace/Facebook). Já documentado no README do projeto para quem for reproduzir.
2. **`opencv-python` 5.0.0 (PyPI)** não inclui os arquivos de cascata Haar — mantenha fixado em `opencv-python==4.10.0.84` nos dois ambientes.
3. **Reprodutibilidade do Dlib:** como foi compilado localmente (não é uma wheel oficial do PyPI), rodar em outra máquina exige repetir o processo de build (CMake + compilador C++ disponível). Se isso for um problema para a banca/reprodução, pode valer a pena excluir o Dlib do resultado final e manter só os 9 modelos com wheel oficial.
4. ~~Ainda não testamos outro detector de rosto (`retinaface`/`yunet`).~~ **RetinaFace testado em 05/10/2026 — ver seção 7.** O YuNet ainda não foi testado.

---

## 6. Conclusão atualizada para a monografia

Cruzando acurácia + tempo (agora medido corretamente, isolado) + tamanho, a dupla mais recomendada continua:

- **ArcFace** — melhor acurácia (92,7%), tempo aceitável (0,74s isolado), tamanho moderado (130 MB, ou poucos MB na variante MobileFaceNet).
- **SFace** — agora confirmado como o mais rápido de todos (0,089s/par) e o menor em disco (5 MB), com 100% de precisão. Antes da correção de isolamento, esse resultado estava mascarado — vale destacar esse achado metodológico na monografia, já que ele muda a conclusão sobre qual modelo é "leve" de verdade.

**Atualização (seção 7):** com o detector RetinaFace, o VGG-Face também passa de 90% (95,57%) e o SFace não melhora (79,69%) — a dupla ArcFace + SFace precisa ser reavaliada antes de fechar a escolha dos 2 modelos.

**Próximo passo recomendado:** repetir o benchmark com o detector `yunet` (leve, pensado para edge), para ver se ele chega perto da acurácia do RetinaFace com um custo de detecção menor.

---

## 7. Segunda rodada: detector OpenCV × RetinaFace (05/10/2026)

Os mesmos 384 pares do LFW foram avaliados com dois detectores de rosto, usando a opção `--cache_deteccao` do script: cada imagem é detectada e alinhada **uma única vez**, o recorte do rosto fica salvo, e os 10 modelos rodam sobre esses recortes. O tempo de detecção é medido à parte, por imagem. Os 10 modelos rodaram sem nenhum erro nos dois detectores.

| Modelo | Acurácia OpenCV | Acurácia RetinaFace | Recall OpenCV | Recall RetinaFace | Tempo total/par OpenCV (s) | Tempo total/par RetinaFace (s) |
|---|---|---|---|---|---|---|
| **ArcFace** | 92,97% | **96,61%** | 86,46% | **93,75%** | 0,559 | 1,804 |
| VGG-Face | 88,02% | 95,57% | 78,65% | 93,75% | 1,064 | 2,340 |
| Dlib | 84,64% | 84,90% | 70,83% | 71,88% | 1,078 | 2,297 |
| Facenet | 76,30% | 82,55% | 52,60% | 65,10% | 0,635 | 1,848 |
| GhostFaceNet | 82,03% | 81,77% | 64,06% | 63,54% | 0,515 | 1,706 |
| SFace | 81,25% | 79,69% | 62,50% | 59,38% | **0,086** | 1,280 |
| Facenet512 | 72,66% | 76,56% | 45,31% | 53,12% | 0,638 | 1,922 |
| DeepFace (Facebook) | 60,16% | 55,47% | 33,33% | 69,27% | 13,828 | 4,733 |
| DeepID | 51,56% | 53,12% | 4,17% | 7,81% | 0,067 | 1,263 |
| OpenFace | 50,78% | 51,04% | 1,56% | 2,60% | 0,261 | 1,695 |

Tempo total/par = tempo de reconhecimento do par + 2 × tempo de detecção por imagem (0,0225 s com OpenCV, 0,6184 s com RetinaFace). CSV completo: [benchmark_comparacao_detectores.csv](../pesquisa/resultados/benchmark_comparacao_detectores.csv) · Gráfico: [benchmark_comparacao_detectores.png](../pesquisa/resultados/benchmark_comparacao_detectores.png)

**Leitura:**

- **ArcFace e VGG-Face são os que mais ganham com um detector melhor:** os dois chegam a 93,75% de recall e passam da meta de 90% de acurácia (RNF-03). O VGG-Face, porém, continua o mais pesado em disco (580 MB).
- **Facenet e Facenet512 melhoram** (+6,3 e +3,9 pontos), mas continuam abaixo de 90%.
- **SFace, GhostFaceNet e Dlib praticamente não mudam** — o recall baixo deles não vinha do detector; o limiar padrão do DeepFace passa a ser o suspeito principal.
- **DeepID e OpenFace continuam perto de 50%** com qualquer detector: a limitação é dos próprios modelos.
- **DeepFace (Facebook)** troca precisão por recall com o RetinaFace (recall sobe para 69%, acurácia cai para 55%) — continua não recomendado.
- **O custo é o tempo:** o RetinaFace leva ~0,62 s por imagem em CPU, contra ~0,02 s do Haar. Com ele, o ArcFace vai a 1,80 s por par, perto do limite de 2 s do RNF-02 — medido no PC, sem o acelerador Hailo.

**Nota de método:** a coluna "OpenCV" desta tabela vem da rodada com cache e não é idêntica à tabela da seção 1 (ex.: ArcFace 92,97% × 92,71%; SFace 0,041 s × 0,089 s de reconhecimento por par). Com o cache, o rosto é detectado **e alinhado** uma vez, e o tempo de reconhecimento é medido sem a detecção; na seção 1, o `DeepFace.verify` detecta as duas imagens a cada par. Para comparar detectores, use esta tabela; a da seção 1 continua valendo como a primeira rodada.
