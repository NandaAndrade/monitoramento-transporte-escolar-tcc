# Guia de leitura: Eigenfaces (Turk e Pentland, 1991)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (MIT Press), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** TURK, M.; PENTLAND, A. Eigenfaces for recognition. *Journal of Cognitive Neuroscience*, v. 3, n. 1, p. 71–86, 1991. DOI: [10.1162/jocn.1991.3.1.71](https://doi.org/10.1162/jocn.1991.3.1.71).
> **PDF local:** `Downloads/Referencias/turk_1991_eigenfaces.pdf` · **Chave no .bib:** `turk1991eigenfaces`

---

## Em uma frase

Os autores mostram que dá para reconhecer rostos rapidamente representando cada um como uma combinação de poucas "imagens-base" (as *eigenfaces*), obtidas por análise de componentes principais (PCA).

## O problema

No fim dos anos 1980, as abordagens dominantes tentavam medir partes do rosto (distância entre os olhos, largura do nariz etc.) ou reconstruir a geometria 3D da cabeça. Isso era lento e frágil. Os autores querem um sistema quase em tempo real, que localize a cabeça em vídeo e reconheça a pessoa.

## A ideia central

1. Uma imagem de rosto de N × N pixels é tratada como um ponto em um espaço de N² dimensões. Como rostos se parecem entre si, esses pontos ocupam só uma pequena região desse espaço.
2. A PCA encontra as direções em que as fotos de treino mais variam. Cada direção, vista como imagem, parece um "rosto fantasma": é uma *eigenface*.
3. Um truque de álgebra torna o cálculo viável: em vez de decompor uma matriz enorme (N² × N²), decompõe-se uma matriz do tamanho do número de fotos de treino (M × M).
4. Cada rosto passa a ser descrito por poucos números, os pesos da sua projeção nas primeiras *eigenfaces*. Reconhecer é achar a pessoa cadastrada com os pesos mais próximos.
5. A mesma projeção serve para detectar se há um rosto na imagem: se a imagem fica longe do "espaço de rostos" (erro de reconstrução alto), não é rosto; se é rosto, mas longe de todas as pessoas cadastradas, é um desconhecido.

## O que foi testado

- Base própria com cerca de 2.500 imagens de 16 pessoas, variando iluminação, orientação da cabeça e tamanho da imagem.
- Classificando todas as imagens como conhecidas, a acerto médio foi de cerca de 96% sob variação de luz, 85% sob variação de orientação e 64% sob variação de tamanho.
- Ao permitir que o sistema rejeite casos duvidosos (limiar de distância), a acurácia sobe, mas parte das imagens deixa de ser classificada: é a troca entre errar e não responder.
- O sistema rodava quase em tempo real no hardware da época, usando movimento no vídeo para achar a cabeça.

## Limitações (apontadas pelos próprios autores ou evidentes hoje)

- Muito sensível a tamanho, orientação e iluminação: as primeiras componentes da PCA captam variação de luz, não de identidade (é o ponto atacado pelo Fisherfaces).
- Testado com poucas pessoas e em condições controladas.
- Exige rostos alinhados e de tamanho semelhante.

## Ligação com o TCC

- Entra na revisão bibliográfica como marco histórico, já citado na Visão Geral.
- O conceito de "projetar o rosto em um espaço de poucas dimensões e comparar distâncias" é o mesmo que os *embeddings* modernos usam (ArcFace, SFace); a diferença é que hoje o espaço é aprendido por uma rede profunda.
- A ideia de usar um limiar para responder "desconhecido" é exatamente o que o projeto precisa para não registrar o aluno errado (RNF-03).
- O artigo de Elngar e Kayed (2020), traduzido nesta pasta, ainda usa esse método em 2020.

## Perguntas para conferir a leitura

1. Por que o truque da matriz M × M é essencial para o método ser viável?
2. Qual a diferença entre "distância ao espaço de rostos" e "distância a uma pessoa cadastrada"?
3. Por que a variação de tamanho prejudicou mais que a de iluminação nos testes?
