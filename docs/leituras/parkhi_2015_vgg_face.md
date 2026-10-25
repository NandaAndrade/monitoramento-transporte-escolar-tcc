# Guia de leitura: VGG-Face, reconhecimento facial profundo (Parkhi *et al.*, 2015)

> **Guia de estudo em português**, não é tradução. O artigo pode ser distribuído sem alterações, mas não tem licença aberta que permita tradução, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** PARKHI, O. M.; VEDALDI, A.; ZISSERMAN, A. Deep Face Recognition. In: *British Machine Vision Conference (BMVC)*, 2015. Páginas a conferir.
> **PDF local:** `docs/Referencias/parkhi_2015_vgg_face.pdf` · **Chave no .bib:** `parkhi2015vggface`

---

## Em uma frase

Os autores do grupo VGG (Oxford) mostram que dá para chegar perto dos sistemas do Google e do Facebook com uma base de treino montada a partir da internet, muito menor, e uma rede convolucional "muito profunda" relativamente simples.

## O problema

Em 2015, os melhores resultados (DeepFace do Facebook, FaceNet do Google) usavam bases privadas de milhões a centenas de milhões de fotos. Pesquisadores fora dessas empresas não tinham dados para treinar redes comparáveis.

## As duas contribuições

### 1. Montar a base de treino com pouco trabalho manual

A base tem **2,6 milhões de imagens de 2.622 pessoas** (celebridades e figuras públicas), montada em cinco etapas:

1. Lista de nomes candidatos e filtragem por pessoas, para garantir fotos suficientes e nenhuma sobreposição com as bases de teste.
2. Busca de imagens no Google e no Bing para cada nome (cerca de 2.000 imagens por pessoa).
3. Filtro automático: um classificador treinado com as primeiras imagens da busca remove rostos errados.
4. Remoção de imagens duplicadas ou quase duplicadas.
5. Revisão manual final, com as imagens já ordenadas pelo classificador para reduzir o esforço.

O trabalho manual total foi de cerca de 14 dias. Um resultado curioso: a rede treinada com a base antes da revisão manual (mais imagens, com mais erros) foi **melhor** que a treinada com a base revisada.

### 2. Treinar a rede e o *embedding*

- A rede segue o estilo VGG: uma longa sequência de camadas convolucionais, com entrada de 224 × 224 pixels e descritor final de 4.096 dimensões.
- Primeiro, a rede é treinada como classificador (uma saída por pessoa). Depois, só a última camada é ajustada com a *triplet loss*, como no FaceNet, para gerar um *embedding* próprio para comparar rostos.

## Resultados principais

- **98,95% na LFW**, com uma única rede e 2,6 milhões de imagens, perto do DeepFace (97,35%, com 4 milhões de imagens e 3 redes) e do FaceNet (que usou 200 milhões).
- **97,3% na YouTube Faces**, estado da arte em vídeo na época.
- O ajuste com *triplet loss* melhora bastante a verificação, e o alinhamento 2D no teste ajuda um pouco.

## Limitações

- O modelo é grande: no benchmark do TCC, o VGG-Face ocupa cerca de 580 MB, o maior dos dez avaliados.
- As celebridades da base são adultas, e a maioria das fotos é profissional.
- O artigo não mede tempo de execução nem uso em hardware pequeno.

## Ligação com o TCC

- **É o segundo colocado do benchmark:** 88,02% de acurácia com o detector do OpenCV e 95,57% com o RetinaFace, acima da meta de 90%. É o principal candidato a "segundo modelo" ao lado do ArcFace.
- O tamanho (580 MB) é o ponto fraco para o Raspberry Pi e para o acelerador Hailo. Pesa na decisão da Atividade 1.3.
- A observação de que mais dados com algum erro valem mais do que poucos dados limpos ajuda a entender por que os modelos treinados com bases enormes (FaceNet, ArcFace) dominam.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Como os autores montaram uma base de 2,6 milhões de imagens com só cerca de 14 dias de trabalho manual?
2. Por que a rede treinada com a base sem revisão manual foi melhor?
3. Qual o papel da *triplet loss* no VGG-Face, e em que ele difere do FaceNet?
4. Qual a principal desvantagem do VGG-Face para o dispositivo do projeto?
