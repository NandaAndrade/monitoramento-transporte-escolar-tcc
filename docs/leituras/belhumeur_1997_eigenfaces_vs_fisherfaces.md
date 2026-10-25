# Guia de leitura: Eigenfaces × Fisherfaces (Belhumeur, Hespanha e Kriegman, 1997)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** BELHUMEUR, P. N.; HESPANHA, J. P.; KRIEGMAN, D. J. Eigenfaces vs. Fisherfaces: recognition using class specific linear projection. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, v. 19, n. 7, p. 711–720, 1997. DOI: [10.1109/34.598228](https://doi.org/10.1109/34.598228).
> **PDF local:** `Downloads/Referencias/belhumeur_1997_eigenfaces_vs_fisherfaces.pdf` · **Chave no .bib:** `belhumeur1997eigenfaces`
>
> **Atenção:** o PDF desta pasta é uma digitalização sem texto extraível, então este guia foi escrito a partir do conteúdo conhecido do artigo, sem conferir os números no PDF. Confira os valores das tabelas no original antes de citá-los.

---

## Em uma frase

Trocar a PCA (Eigenfaces) pela análise discriminante linear de Fisher (Fisherfaces) torna o reconhecimento facial muito mais robusto a mudanças de iluminação e de expressão.

## O problema

As *eigenfaces* guardam as direções em que as imagens mais variam. Mas, entre fotos de rostos, a maior variação costuma vir da luz, não da identidade: duas fotos da mesma pessoa com luz diferente podem ficar mais distantes entre si do que fotos de pessoas diferentes com a mesma luz. A PCA não sabe quem é quem no treino, então não consegue separar esses dois tipos de variação.

## A ideia central

1. A análise discriminante linear (LDA) usa os rótulos do treino: busca uma projeção que **afaste as médias de pessoas diferentes** e, ao mesmo tempo, **junte as fotos de uma mesma pessoa** (maximiza a razão entre dispersão entre classes e dispersão dentro das classes).
2. Problema prático: com poucas fotos por pessoa, a matriz de dispersão dentro das classes é singular e a LDA não pode ser aplicada direto. A solução é aplicar primeiro uma PCA para reduzir a dimensão e só então a LDA. Essa combinação é o *Fisherfaces*.
3. Os autores ligam isso a um argumento físico: sob certas hipóteses (superfície que reflete a luz de forma difusa, sem sombras), todas as imagens de um rosto sob iluminações diferentes ficam em um subespaço de dimensão baixa. Uma projeção linear bem escolhida pode, portanto, "ignorar" boa parte da variação de luz.

## O que foi testado

- Duas bases: uma da Harvard, com variação controlada da direção da luz, e a base Yale, com variação de luz, expressão facial e uso de óculos.
- Comparação entre correlação direta das imagens, Eigenfaces, Eigenfaces sem as três primeiras componentes (que concentram efeito de luz), espaço linear por pessoa e Fisherfaces.
- O Fisherfaces teve as menores taxas de erro, principalmente com luz extrema e com mudanças de expressão. Uma observação curiosa: descartar as primeiras componentes da PCA melhora o Eigenfaces, confirmando que elas codificam iluminação.
- Teste extra: detectar se a pessoa está de óculos, em que o Fisherfaces também se saiu melhor.

## Limitações

- Bases pequenas e controladas (poucas dezenas de pessoas).
- É uma projeção linear; pose (rosto de lado) continua sendo um problema sério.
- Precisa retreinar a projeção quando novas pessoas são cadastradas.

## Ligação com o TCC

- Marco histórico na revisão bibliográfica, junto com o Eigenfaces.
- A ideia de "juntar a mesma pessoa e afastar pessoas diferentes" é a mesma que as perdas modernas, como a ArcFace e a SFace, buscam, só que com redes profundas e no espaço angular.
- Lembrete prático para o projeto: a luz dentro do ônibus (sol pela janela, contraluz na porta) é justamente o fator que derrubava os métodos clássicos.

## Perguntas para conferir a leitura

1. Por que a PCA pode piorar o reconhecimento quando a iluminação varia muito?
2. Por que é preciso aplicar uma PCA antes da LDA no Fisherfaces?
3. O que acontece com o Fisherfaces quando um aluno novo é cadastrado? Compare com um sistema baseado em *embeddings*.
