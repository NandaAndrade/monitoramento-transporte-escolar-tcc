# Guia de leitura: FaceNet (Schroff, Kalenichenko e Philbin, 2015)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE; versão aberta no arXiv), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** SCHROFF, F.; KALENICHENKO, D.; PHILBIN, J. FaceNet: a unified embedding for face recognition and clustering. In: IEEE CVPR, 2015. *Proceedings* [...]. p. 815–823. DOI: [10.1109/CVPR.2015.7298682](https://doi.org/10.1109/CVPR.2015.7298682) · versão aberta: [arXiv 1503.03832](https://arxiv.org/abs/1503.03832).
> **PDF local:** `Downloads/Referencias/schroff_2015_facenet.pdf` · **Chave no .bib:** `schroff2015facenet`

---

## Em uma frase

O FaceNet treina uma rede para levar cada foto de rosto a um vetor de 128 números (*embedding*), de forma que a **distância entre vetores já seja a medida de semelhança** entre rostos; com isso, verificar, identificar e agrupar pessoas vira só comparar distâncias.

## O problema

Antes dele, as redes profundas de reconhecimento facial eram treinadas como classificadores (uma saída por pessoa do treino) e depois se usava uma camada intermediária como descritor. Isso é indireto: a rede não foi treinada para que essa camada tenha boas distâncias, e o descritor ficava grande.

## A ideia central: a *triplet loss*

1. O treino usa trios de imagens: uma **âncora**, uma **positiva** (mesma pessoa) e uma **negativa** (outra pessoa).
2. A perda pede que a âncora fique mais perto da positiva do que da negativa, com uma **margem** de folga. Se isso já acontece, o trio não contribui.
3. Os vetores são normalizados para ficar sobre uma hiperesfera, o que deixa as distâncias comparáveis.
4. O ponto delicado é **escolher bons trios**. Trios fáceis não ensinam nada; os mais difíceis possíveis atrapalham o início do treino. Os autores escolhem os trios dentro de cada lote, durante o treino, priorizando negativos "semidifíceis": mais longe que a positiva, mas ainda dentro da margem.

## Arquiteturas e dados

- Testaram duas famílias de redes: uma derivada da rede de Zeiler e Fergus e outra baseada na Inception (GoogLeNet), mais eficiente em parâmetros e operações. Também mostram versões menores, pensadas para celulares.
- O treino usou uma base interna do Google, gigantesca: de 100 a 200 milhões de fotos de cerca de 8 milhões de pessoas.

## Resultados principais

- 99,63% de acurácia na LFW, então recorde.
- 95,12% na base de vídeos YouTube Faces.
- O *embedding* ocupa só 128 bytes por rosto, e o desempenho cai pouco ao reduzir a dimensão.
- Os autores mostram também agrupamento: fotos da mesma pessoa em idades e condições diferentes caem no mesmo grupo.

## Limitações

- Depende de uma base de treino enorme e privada, impossível de reproduzir fora do Google.
- A escolha dos trios é trabalhosa e o treino converge devagar. Perdas posteriores, como a ArcFace, chegam a resultados melhores com treino mais simples.

## Ligação com o TCC

- É a base conceitual dos *embeddings*: o sistema do projeto cadastra o vetor de cada aluno e compara distâncias, sem retreinar a rede para cada aluno novo.
- Os modelos Facenet e Facenet512 do benchmark são reimplementações desta ideia (pela biblioteca DeepFace), não o modelo original do Google.
- A noção de **margem** e de **limiar de distância** é a que o projeto precisa calibrar para priorizar a precisão (RNF-03).
- O FN8, de Deng *et al.* (2023), traduzido nesta pasta, é uma versão encolhida do FaceNet para hardware fraco.

## Perguntas para conferir a leitura

1. Por que escolher só os trios mais difíceis atrapalha o treino?
2. Qual a vantagem de treinar o *embedding* diretamente, em vez de usar a camada de um classificador?
3. Como um sistema baseado em *embedding* lida com um aluno novo, sem retreinar a rede?
