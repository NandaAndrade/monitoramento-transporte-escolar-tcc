# Guia de leitura: base AT&T/ORL e modelos ocultos de Markov para rostos (Samaria e Harter, 1994)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** SAMARIA, F. S.; HARTER, A. C. Parameterisation of a stochastic model for human face identification. In: IEEE WORKSHOP ON APPLICATIONS OF COMPUTER VISION, 1994. *Proceedings* [...]. 1994. p. 138–142. DOI: [10.1109/ACV.1994.341300](https://doi.org/10.1109/ACV.1994.341300).
> **PDF local:** `Downloads/Referencias/samaria_1994_base_att_orl.pdf` · **Chave no .bib:** `samaria1994att`
>
> **Atenção:** o texto do PDF desta pasta não pôde ser extraído (fontes embutidas sem mapeamento de caracteres), então este guia foi escrito a partir do conteúdo conhecido do artigo. Confira os valores numéricos no original antes de citá-los.

---

## Em uma frase

O artigo propõe reconhecer rostos com modelos ocultos de Markov (HMM) e, para testá-lo, cria a base de rostos que ficou conhecida como ORL ou AT&T, até hoje usada como referência.

## Por que este artigo está na bibliografia

O projeto usa a **base AT&T/ORL** (em `pesquisa/dados/att/`), e este é o artigo que se cita quando se usa essa base. O método em si (HMM) é histórico e não é usado no TCC.

## A base de dados

- Montada no Olivetti Research Laboratory, em Cambridge (Reino Unido), entre 1992 e 1994.
- 40 pessoas, 10 fotos de cada uma, total de 400 imagens.
- Imagens em tons de cinza, 92 × 112 pixels, fundo escuro e uniforme, pessoa de frente.
- Variações pequenas e controladas: momento da foto, iluminação levemente diferente, expressão (olhos abertos ou fechados, sorrindo ou não), uso de óculos e uma pequena inclinação da cabeça.
- Protocolo usado no artigo: 5 fotos de cada pessoa para treinar e 5 para testar.

## A ideia do método

1. Um rosto de frente tem uma ordem fixa de regiões de cima para baixo: testa, olhos, nariz, boca, queixo.
2. O HMM modela essa sequência: cada "estado" corresponde a uma região, e a imagem é lida como uma sequência de faixas horizontais, que se sobrepõem um pouco.
3. Treina-se um HMM por pessoa. Para reconhecer, calcula-se qual modelo explica melhor a sequência de faixas da foto de teste.
4. O foco do artigo é a **parametrização**: como a altura das faixas, a sobreposição entre elas e o número de estados afetam a taxa de erro. Os autores mostram que essas escolhas mudam bastante o resultado.

## Limitações

- Base pequena e controlada: 40 pessoas adultas, de frente, com fundo uniforme. Taxas de acerto altas nela dizem pouco sobre condições reais.
- O método supõe rosto de frente e bem enquadrado.

## Ligação com o TCC

- Citar este artigo sempre que a base AT&T for usada.
- Útil como **contraste** com a LFW: a AT&T mostra o desempenho em condições ideais, e a LFW, em condições não controladas. A distância entre as duas dá uma ideia de quanto as condições do ônibus podem pesar.
- Cuidado ao comparar números: os artigos de Elngar e Kayed (2020) e de Meddeb *et al.* (2023), que estão nesta pasta, relatam acurácias altas na ORL, mas isso não indica desempenho em ambiente real (item E3 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).

## Perguntas para conferir a leitura

1. Por que a ordem "testa → olhos → nariz → boca → queixo" torna o HMM uma escolha natural para rostos de frente?
2. Que características da base AT&T a tornam mais fácil que a LFW?
3. Por que 5 fotos de treino por pessoa é uma condição diferente da do projeto, em que cada aluno terá poucas fotos de cadastro?
