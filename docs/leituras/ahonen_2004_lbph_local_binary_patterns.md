# Guia de leitura: reconhecimento facial com padrões binários locais (Ahonen, Hadid e Pietikäinen, 2004)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (Springer), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** AHONEN, T.; HADID, A.; PIETIKÄINEN, M. Face recognition with local binary patterns. In: COMPUTER VISION – ECCV 2004. Berlin: Springer, 2004. p. 469–481. (Lecture Notes in Computer Science, v. 3021). DOI: [10.1007/978-3-540-24670-1_36](https://doi.org/10.1007/978-3-540-24670-1_36).
> **PDF local:** `Downloads/Referencias/ahonen_2004_lbph_local_binary_patterns.pdf` · **Chave no .bib:** `ahonen2004face`

---

## Em uma frase

Descrever o rosto pela **textura local** (padrões binários locais) em várias regiões, e comparar os histogramas dessas regiões, dá um reconhecimento simples, rápido e mais robusto que a PCA. É o método conhecido como **LBPH**.

## O operador LBP, em termos simples

1. Para cada pixel, compara-se sua intensidade com a dos 8 vizinhos ao redor.
2. Cada vizinho vira um bit: 1 se for mais claro ou igual ao pixel central, 0 se for mais escuro.
3. Os 8 bits formam um número de 0 a 255, que descreve a "forma" local da textura (borda, canto, ponto, área lisa).
4. Como só importa quem é mais claro que quem, o código não muda se a imagem inteira ficar mais clara ou mais escura: daí a robustez a mudanças **uniformes** de iluminação.
5. Os autores usam uma versão com vizinhança circular e só os padrões "uniformes" (com no máximo duas transições entre 0 e 1), que concentram a maior parte da informação e reduzem o tamanho do histograma.

## Como o rosto é descrito

1. A imagem do rosto é dividida em uma grade de pequenas regiões (por exemplo, 7 × 7).
2. Em cada região, calcula-se o histograma dos códigos LBP.
3. Os histogramas de todas as regiões são concatenados em um único vetor. Assim, o descritor guarda o "que textura existe" e o "onde ela está".
4. A comparação entre dois rostos usa a distância qui-quadrado entre os histogramas, com **pesos por região**: olhos e boca pesam mais; bochechas e testa, menos.
5. A classificação é pelo vizinho mais próximo.

## O que foi testado

- Base FERET, padrão da época, com quatro conjuntos de teste: mudança de expressão (fb), mudança de iluminação (fc) e fotos tiradas tempos depois (dup I e dup II).
- O LBP com pesos teve acerto de 0,97 (expressão), 0,79 (iluminação), 0,66 e 0,64 (envelhecimento), à frente da PCA, do classificador bayesiano e do casamento elástico de grafos (EBGM) em todos os conjuntos.
- Os autores também estudam o tamanho das regiões, o raio e o número de vizinhos do operador, e como escolher os pesos das regiões.

## Limitações

- Robusto a luz uniforme, mas não a sombras fortes de um lado do rosto.
- Pose (rosto de lado) continua sendo problema.
- Exige rosto alinhado, porque a grade de regiões depende da posição dos olhos e da boca.

## Ligação com o TCC

- Marco histórico na revisão bibliográfica, já citado na Visão Geral.
- O LBPH ainda aparece em sistemas de presença de baixo custo, inclusive no OpenCV; serve de contraste com os modelos profundos testados no benchmark.
- O artigo de Jha *et al.* (2024), traduzido nesta pasta, usa LBP combinado com Gabor para detectar vivacidade, o que mostra que a ideia continua útil como característica complementar.

## Perguntas para conferir a leitura

1. Por que o código LBP não muda quando a imagem inteira fica mais clara?
2. Para que serve dividir o rosto em regiões antes de calcular os histogramas?
3. Por que olhos e boca recebem mais peso que as bochechas?
