# Relatório — Benchmark de Reconhecimento Facial (TCC)

**Dataset:** LFW (Labeled Faces in the Wild), 96 pessoas com ≥15 fotos cada, baixado via `scikit-learn`.
**Pares avaliados por modelo:** 384 (192 positivos / mesma pessoa + 192 negativos / pessoas diferentes).
**Detector de rosto:** OpenCV (Haar Cascade) — o mais leve dos disponíveis, mais próximo do custo aceitável em Raspberry Pi/Hailo. Comparado com o RetinaFace na seção 7 e com o YuNet na seção 8.
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
4. ~~Ainda não testamos outro detector de rosto (`retinaface`/`yunet`).~~ **RetinaFace testado em 05/10/2026 — ver seção 7. YuNet testado em 25/10/2026 — ver seção 8.**

---

## 6. Conclusão atualizada para a monografia

Cruzando acurácia + tempo (agora medido corretamente, isolado) + tamanho, a dupla mais recomendada continua:

- **ArcFace** — melhor acurácia (92,7%), tempo aceitável (0,74s isolado), tamanho moderado (130 MB, ou poucos MB na variante MobileFaceNet).
- **SFace** — agora confirmado como o mais rápido de todos (0,089s/par) e o menor em disco (5 MB), com 100% de precisão. Antes da correção de isolamento, esse resultado estava mascarado — vale destacar esse achado metodológico na monografia, já que ele muda a conclusão sobre qual modelo é "leve" de verdade.

**Atualização (seção 7):** com o detector RetinaFace, o VGG-Face também passa de 90% (95,57%) e o SFace não melhora (79,69%) — a dupla ArcFace + SFace precisa ser reavaliada antes de fechar a escolha dos 2 modelos.

**Próximo passo recomendado:** ~~repetir o benchmark com o detector `yunet`~~ (feito em 25/10/2026, seção 8). Agora: calibrar o limiar de decisão de cada modelo priorizando a precisão (RNF-03) antes de fechar os 2 modelos.

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

---

## 8. Terceira rodada: detector YuNet (25/10/2026)

Mesma metodologia da seção 7: os mesmos 384 pares do LFW, `--cache_deteccao` (cada imagem é detectada e alinhada uma única vez) e cada modelo em um processo isolado. O YuNet é o detector padrão do OpenCV (`cv2.FaceDetectorYN`, modelo `face_detection_yunet_2023mar.onnx`), com 75.856 parâmetros.

### 8.1 Desafio: o YuNet "perdia" 10% dos rostos dentro do DeepFace

Na primeira tentativa, o YuNet devolveu **"nenhum rosto" em 65 das 649 imagens (10%)**. Com `enforce_detection=False`, o DeepFace usa a foto inteira no lugar do recorte, então esses pares eram comparados sem detecção nem alinhamento. O VGG-Face, por exemplo, caiu de 95,57% (RetinaFace) para 93,23%.

**Investigação:**

1. **O limiar sozinho não explicava.** O DeepFace usa confiança mínima de 0,9 para o YuNet, lida da variável de ambiente `yunet_score_threshold`. Mas, chamando o YuNet direto (fora do DeepFace) nas 65 imagens com o mesmo limiar de 0,9, ele achou o rosto em 64.
2. **A diferença estava no pré-processamento do DeepFace.** Com `align=True`, `deepface/modules/detection.py` coloca uma **borda preta de 50% da altura e da largura** em volta da imagem antes de detectar. O objetivo é que o rosto não saia do quadro quando é girado no alinhamento. Nas fotos do LFW, que têm só 94×125 px, o rosto passa a ocupar uma fração bem menor do quadro e a confiança do YuNet cai abaixo de 0,9.
3. **Teste isolado nas 65 imagens que falharam:**

| | Limiar 0,9 | Limiar 0,5 |
|---|---|---|
| Sem a borda | 64/65 detectadas | 65/65 |
| Com a borda do DeepFace | **3/65** | **65/65** |

**Solução:** o script passou a usar **limiar de 0,5 para o YuNet**. Esse é o valor usado no artigo do YuNet (Wu; Peng; Yu, 2023), e com ele nenhum rosto se perde. O valor fica na constante `LIMIAR_CONFIANCA_YUNET` de [benchmark_reconhecimento_facial.py](../pesquisa/benchmark_reconhecimento_facial.py), que define a variável de ambiente antes da detecção; os processos isolados de cada modelo a herdam. Se a variável já estiver definida no ambiente, o valor dela é respeitado, para permitir repetir a rodada com outro limiar. Baixar o limiar não traz rostos falsos para o recorte, porque o script fica só com o rosto de maior área de cada imagem.

**Por que isso importa para o TCC:**

- **É um efeito da combinação biblioteca + imagem pequena, não do YuNet.** O mesmo pode acontecer no dispositivo se a câmera entregar quadros pequenos ou se o rosto ocupar pouco do quadro. O adaptador definitivo deve chamar o YuNet direto (sem a borda do DeepFace) e ter o limiar na configuração, como manda a seção 5 de [arquitetura.md](arquitetura.md).
- **O DeepFace troca "nenhum rosto" pela imagem inteira sem avisar.** Com `enforce_detection=False`, a falha só apareceu porque contamos os recortes do mesmo tamanho da foto original. Vale registrar na monografia quantas imagens ficaram sem rosto em cada detector.
- É o mesmo tipo de problema já visto com o RetinaFace: um padrão da biblioteca que não combina com as fotos pequenas do LFW (a ampliação até 1024 px, desligada na rodada da seção 7).

**Problema menor no caminho:** com a saída redirecionada para arquivo no Windows, o Python usa a codificação cp1252, e o aviso do DeepFace com emoji derruba o script com `UnicodeEncodeError` antes de começar. Resolve-se definindo `PYTHONIOENCODING=utf-8` (ou `PYTHONUTF8=1`) antes de rodar.

### 8.2 Rodada descartada (limiar 0,9)

Guardada só como registro do problema, em [benchmark_resultados_yunet_limiar09.csv](../pesquisa/resultados/benchmark_resultados_yunet_limiar09.csv). Não entra na comparação entre detectores. O DeepFace (Facebook) não foi rodado nessa configuração.

| Modelo | Acurácia | Recall | Reconhecimento/par (s) |
|---|---|---|---|
| ArcFace | 94,53% | 90,62% | 0,622 |
| VGG-Face | 93,23% | 90,10% | 1,498 |
| Dlib | 82,29% | 66,67% | 0,953 |
| Facenet | 82,03% | 64,06% | 0,726 |
| GhostFaceNet | 76,82% | 54,69% | 0,519 |
| SFace | 76,04% | 53,12% | 0,038 |
| Facenet512 | 75,78% | 51,56% | 0,727 |
| DeepID | 53,65% | 9,38% | 0,027 |
| OpenFace | 50,52% | 1,04% | 0,253 |

Detecção: 0,022 s por imagem em média (mediana de 0,012 s), contra 0,618 s do RetinaFace.

### 8.3 Resultados com limiar 0,5: comparação dos três detectores

Com o limiar de 0,5, só 3 das 649 imagens (0,5%) ficaram sem rosto, contra 65 com 0,9. Os 10 modelos rodaram sem nenhum erro; o DeepFace (Facebook) rodou no ambiente legado sobre o mesmo cache.

| Modelo | Acurácia OpenCV | Acurácia RetinaFace | Acurácia YuNet | Recall YuNet | Tempo total/par OpenCV (s) | Tempo total/par RetinaFace (s) | Tempo total/par YuNet (s) |
|---|---|---|---|---|---|---|---|
| **ArcFace** | 92,97% | **96,61%** | 95,57% | 92,19% | 0,559 | 1,804 | 0,586 |
| VGG-Face | 88,02% | 95,57% | 93,75% | 91,15% | 1,064 | 2,340 | 1,286 |
| Dlib | 84,64% | 84,90% | 82,29% | 67,19% | 1,078 | 2,297 | 0,868 |
| Facenet | 76,30% | 82,55% | 81,51% | 63,02% | 0,635 | 1,848 | 0,732 |
| GhostFaceNet | 82,03% | 81,77% | 77,86% | 56,77% | 0,515 | 1,706 | 0,586 |
| SFace | 81,25% | 79,69% | 75,00% | 51,56% | 0,086 | 1,280 | **0,070** |
| Facenet512 | 72,66% | 76,56% | 76,04% | 52,08% | 0,638 | 1,922 | 0,745 |
| DeepFace (Facebook) | 60,16% | 55,47% | 58,85% | 39,58% | 13,828 | 4,733 | 4,215 |
| DeepID | 51,56% | 53,12% | 53,39% | 8,85% | 0,067 | 1,263 | 0,045 |
| OpenFace | 50,78% | 51,04% | 50,52% | 1,04% | 0,261 | 1,695 | 0,307 |

Tempo de detecção por imagem: **0,0074 s com YuNet**, 0,0225 s com OpenCV (Haar) e 0,6184 s com RetinaFace. CSV completo: [benchmark_resultados_yunet.csv](../pesquisa/resultados/benchmark_resultados_yunet.csv) e [benchmark_comparacao_detectores.csv](../pesquisa/resultados/benchmark_comparacao_detectores.csv) · Gráfico: [benchmark_comparacao_detectores.png](../pesquisa/resultados/benchmark_comparacao_detectores.png). O script [comparar_detectores.py](../pesquisa/comparar_detectores.py) passou a juntar os três detectores.

**Leitura:**

- **O YuNet é o detector mais rápido dos três:** cerca de 3 vezes mais rápido que o Haar e 80 vezes mais rápido que o RetinaFace, no PC. Isso confirma o que a literatura indicava.
- **Para ArcFace e VGG-Face, o YuNet chega perto do RetinaFace:** o ArcFace fica 1 ponto abaixo (95,57% × 96,61%) e o VGG-Face, 1,8 ponto. Os dois continuam acima da meta de 90% (RNF-03). O tempo total do ArcFace cai de 1,80 s para 0,59 s por par, bem longe do limite de 2 s (RNF-02).
- **Para SFace, GhostFaceNet e Dlib, o YuNet é o pior dos três detectores** (SFace: 75,00% contra 81,25% com Haar). Uma hipótese é a diferença no recorte e no alinhamento: cada detector devolve uma caixa e pontos do rosto um pouco diferentes, e o limiar de decisão padrão do DeepFace para cada modelo não foi ajustado para esses recortes. A precisão continua alta e o recall baixo, o mesmo padrão das rodadas anteriores. Por isso, só a calibração do limiar (M2 de [lacunas_revisao_bibliografica.md](lacunas_revisao_bibliografica.md)) vai dizer se a diferença é do detector ou do limiar.
- **DeepID e OpenFace seguem perto de 50%** com qualquer detector, e o **DeepFace (Facebook)** continua o pior custo-benefício.
- **As diferenças pequenas não são conclusivas:** com 384 pares, a margem de erro fica em cerca de ±2 pontos (M6), então ArcFace com YuNet e com RetinaFace estão empatados estatisticamente.

**Conclusão parcial:** a combinação **YuNet + ArcFace** é a que melhor atende aos dois requisitos ao mesmo tempo nesta amostra: 95,57% de acurácia e 0,59 s por par no PC. O RetinaFace só se justificaria se as condições do ônibus derrubarem a detecção do YuNet. A escolha dos 2 modelos ainda depende da calibração do limiar, que pode mudar a posição de SFace e GhostFaceNet.
