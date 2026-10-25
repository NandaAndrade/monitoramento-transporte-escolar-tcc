# Guia de leitura: DeepFace, do Facebook (Taigman *et al.*, 2014)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** TAIGMAN, Y.; YANG, M.; RANZATO, M.; WOLF, L. DeepFace: Closing the Gap to Human-Level Performance in Face Verification. In: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2014. Páginas a conferir.
> **PDF local:** `docs/Referencias/taigman_2014_deepface.pdf` · **Chave no .bib:** `taigman2014deepface`
>
> **Atenção ao nome:** "DeepFace" é tanto este modelo do Facebook quanto a biblioteca Python de Serengil e Ozpinar usada no benchmark (ver `serengil_2020_lightface_biblioteca_deepface.md`). A biblioteca oferece este modelo como uma das dez opções.

---

## Em uma frase

O DeepFace foi o primeiro sistema a chegar perto do desempenho humano na LFW (97,35%, contra 97,53% de humanos), combinando um alinhamento 3D do rosto com uma rede profunda treinada em 4,4 milhões de fotos do Facebook.

## O problema

O processo padrão de reconhecimento facial tem quatro etapas: detectar, alinhar, representar e classificar. Os autores revisitam duas delas: o **alinhamento**, que até então era só 2D, e a **representação**, que dependia de descritores feitos à mão.

## A ideia central

1. **Alinhamento 3D:** o rosto detectado é primeiro alinhado em 2D por 6 pontos. Depois, 67 pontos de referência são localizados e encaixados num modelo 3D genérico de rosto, e a imagem é "frontalizada", como se a pessoa estivesse olhando para a câmera.
2. **Rede de nove camadas:** recebe a imagem frontalizada (152 × 152 pixels, colorida). Depois de uma camada convolucional, um *pooling* e outra convolução, vêm **três camadas localmente conectadas**: cada posição da imagem tem filtros próprios, porque, num rosto alinhado, olhos, nariz e boca estão sempre no mesmo lugar. A rede tem mais de **120 milhões de parâmetros**.
3. **Treino como classificador:** a rede aprende a dizer qual das 4.030 pessoas está na foto. A penúltima camada vira a representação do rosto, e a verificação compara essas representações.

## Dados

- **SFC (Social Face Classification):** 4,4 milhões de fotos de 4.030 pessoas, com 800 a 1.200 fotos cada, tiradas do Facebook. As fotos mais recentes de cada pessoa ficaram para teste, para simular o envelhecimento.
- Os autores estimam cerca de 3% de rótulos errados.

## Resultados principais

- **97,35% na LFW** com um conjunto de redes, reduzindo em mais de 27% o erro do melhor método anterior.
- **91,4% na YouTube Faces**, reduzindo o erro anterior em mais de 50%.
- Reduzir a base de treino aumentou o erro de forma clara, e o desempenho não saturou com 4 milhões de imagens: mais dados ainda ajudariam.

## Limitações

- Depende de uma base privada enorme, que outros pesquisadores não podem usar.
- A representação vem de uma rede treinada para classificar as pessoas do treino, não para comparar rostos: o FaceNet, um ano depois, mostrou que treinar o *embedding* diretamente funciona melhor.
- O alinhamento 3D é complexo e caro.
- A rede é pesada (mais de 120 milhões de parâmetros).

## Ligação com o TCC

- **No benchmark, teve um dos piores resultados:** 60,16% de acurácia com o detector do OpenCV e 55,47% com o RetinaFace. Foi também o mais lento: cerca de 13,8 s por par de imagens com o OpenCV, num modelo de cerca de 150 MB. Não serve para o dispositivo.
- É um marco histórico importante: mostra a virada para redes profundas e a importância do alinhamento, retomada pelo Serengil (biblioteca DeepFace) e pelo RetinaFace.
- O contraste com o FaceNet (classificar versus aprender o *embedding*) ajuda a explicar por que os modelos de *embedding* foram os melhores do benchmark.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. O que é a "frontalização" e por que ela ajuda a rede?
2. Por que os autores usaram camadas localmente conectadas em vez de convolucionais nas camadas do meio?
3. Qual a diferença entre a representação do DeepFace e o *embedding* do FaceNet?
4. Que números do benchmark do TCC mostram que o DeepFace não serve para o dispositivo?
