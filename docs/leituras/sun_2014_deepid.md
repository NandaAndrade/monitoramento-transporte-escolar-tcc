# Guia de leitura: DeepID, representação aprendida com 10.000 classes (Sun *et al.*, 2014)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** SUN, Y.; WANG, X.; TANG, X. Deep Learning Face Representation from Predicting 10,000 Classes. In: *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2014. Páginas a conferir.
> **PDF local:** `docs/Referencias/sun_2014_deepid.pdf` · **Chave no .bib:** `sun2014deepid`

---

## Em uma frase

O DeepID treina redes convolucionais para classificar cerca de 10.000 pessoas e usa a última camada escondida, de só 160 números, como representação do rosto; com isso chega a 97,45% na LFW, quase o desempenho humano (97,53%).

## A ideia central

1. **Aprender identificando muitas pessoas.** A tese do artigo é que treinar a rede para distinguir milhares de pessoas ao mesmo tempo força a camada escondida a guardar traços de identidade que servem também para pessoas que a rede nunca viu. Quanto mais pessoas no treino, melhor a verificação.
2. **Representação compacta.** A camada DeepID tem só **160 dimensões** e fica logo antes da saída de classificação. Ela recebe tanto a última camada convolucional quanto a anterior, o que mistura traços em mais de uma escala.
3. **Muitas redes pequenas.** O rosto é dividido em **60 recortes** (10 regiões, 3 escalas, colorido ou em tons de cinza), e cada recorte tem a sua rede. As representações das 60 redes são concatenadas.
4. **Verificação com Joint Bayesian.** Para decidir se dois rostos são da mesma pessoa, os autores usam o Joint Bayesian, um modelo estatístico que separa a variação de identidade da variação dentro de uma mesma pessoa.
5. **Alinhamento fraco.** Só cinco pontos (olhos, ponta do nariz e cantos da boca) são usados para alinhar o rosto, sem modelo 3D, ao contrário do DeepFace.

## Dados

- **CelebFaces:** 87.628 fotos de 5.436 celebridades, cerca de 16 por pessoa.
- **CelebFaces+:** 202.599 fotos de 10.177 celebridades, usada no resultado final.
- Nenhuma pessoa da LFW aparece nas bases de treino.

## Resultados principais

- **97,45% na LFW** com alinhamento fraco, perto dos 97,53% de humanos e acima dos 97,35% do DeepFace.
- Ligar a camada DeepID também à penúltima camada convolucional melhorou a verificação de 95,35% para 96,05% nos experimentos com a base menor.
- A acurácia sobe de forma constante à medida que o número de pessoas no treino aumenta.

## Limitações

- O resultado depende de 60 redes e do Joint Bayesian; uma rede só é bem mais fraca.
- Assim como o DeepFace, a representação vem de um classificador, não de um *embedding* treinado para comparar rostos.
- O artigo não mede tempo de execução.

## Ligação com o TCC

- **No benchmark, ficou entre os piores:** 51,56% com o detector do OpenCV e 53,12% com o RetinaFace, praticamente um chute. O *recall* foi quase zero (4,2% e 7,8%): o modelo quase nunca dizia "mesma pessoa".
- O modelo do DeepID é o menor da lista (cerca de 3 MB) e muito rápido. O resultado ruim provavelmente vem em parte do limiar padrão do DeepFace. Além disso, o artigo combina 60 redes e o Joint Bayesian, enquanto a biblioteca oferece um único modelo pré-treinado (é preciso conferir na documentação da biblioteca como ele foi treinado). Por isso a comparação com os 97,45% do artigo não é justa.
- Serve como exemplo histórico de como a ideia de "aprender a identificar muitas pessoas" levou às perdas com margem, como a do ArcFace.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Por que classificar 10.000 pessoas ajuda a reconhecer pessoas que não estavam no treino?
2. Para que servem os 60 recortes do rosto?
3. Por que o resultado do DeepID no benchmark é tão diferente do artigo?
