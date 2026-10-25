# Guia de leitura: SFace (Zhong *et al.*, 2021)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE; versão aberta no arXiv), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** ZHONG, Y.; DENG, W.; HU, J.; ZHAO, D.; LI, X.; WEN, D. SFace: sigmoid-constrained hypersphere loss for robust face recognition. *IEEE Transactions on Image Processing*, v. 30, p. 2587–2598, 2021. DOI: [10.1109/TIP.2020.3048632](https://doi.org/10.1109/TIP.2020.3048632) · versão aberta: [arXiv 2205.12010](https://arxiv.org/abs/2205.12010).
> **PDF local:** `Downloads/Referencias/zhong_2021_sface.pdf` · **Chave no .bib:** `zhong2021sface`

---

## Em uma frase

A SFace é uma função de perda que, em vez de forçar ao máximo a aproximação de fotos da mesma pessoa e o afastamento de pessoas diferentes, **otimiza de forma moderada**, para não aprender com fotos ruins e rótulos errados das bases de treino.

## O problema

As perdas com margem (como ArcFace e CosFace) seguem um ideal rígido: juntar ao máximo a mesma pessoa e afastar ao máximo as diferentes. Só que bases grandes de treino, montadas a partir da internet, têm fotos borradas, de baixa resolução e com rótulos trocados. Forçar o modelo a encaixar perfeitamente esses exemplos leva a **sobreajuste**: o modelo decora ruído.

## A ideia central

1. Como na ArcFace, os *embeddings* ficam sobre uma hiperesfera e a semelhança é medida por ângulo.
2. A perda tem duas partes separadas: uma que **aproxima** a foto do centro da sua classe e outra que a **afasta** dos centros das outras classes.
3. Cada parte tem o seu gradiente multiplicado por uma **curva sigmoide**. A curva funciona como um "freio": quando o exemplo já está razoavelmente bem posicionado, o empurrão diminui; o modelo não insiste em deixá-lo perfeito.
4. Os parâmetros das duas sigmoides controlam quanto aproximar e quanto afastar, permitindo equilibrar exemplos limpos (que devem ser otimizados) e exemplos ruidosos (que não devem dominar o treino).

## O que foi testado

- Treino em bases grandes (com e sem ruído artificial nos rótulos) e avaliação em LFW, YTF, CALFW, CPLFW, MegaFace, IJB-A e IJB-C, entre outras.
- A SFace ficou à frente ou empatada com as perdas de margem nas bases limpas e se destacou quando havia ruído no treino, que era a proposta.
- O artigo traz análises dos gradientes e da distribuição dos ângulos durante o treino, que ajudam a entender o "freio" das sigmoides.

## Limitações

- Mais hiperparâmetros para ajustar (as duas sigmoides).
- O ganho é maior justamente quando a base de treino é ruidosa; em bases limpas, a vantagem é pequena.

## Ligação com o TCC

- No benchmark, o SFace foi o **mais leve e rápido** (5 MB, cerca de 0,04 s de reconhecimento por par), mas ficou abaixo de 82% de acurácia com o limiar padrão, com precisão de 100% e *recall* baixo. Esse padrão sugere um limiar conservador demais, e não um modelo ruim (item M2 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).
- Na literatura, a diferença entre SFace e ArcFace é pequena; no benchmark, foi de cerca de 17 pontos. A calibração do limiar é o próximo passo para tirar essa dúvida antes de descartar o SFace.
- O modelo SFace tem versão oficial no OpenCV, o que facilita rodar no Raspberry Pi.

## Perguntas para conferir a leitura

1. Por que forçar ao máximo a separação pode piorar o modelo quando a base de treino tem rótulos errados?
2. O que a curva sigmoide faz com o gradiente quando um exemplo já está bem posicionado?
3. Por que "precisão 100% e *recall* baixo" aponta para o limiar, e não para o modelo?
