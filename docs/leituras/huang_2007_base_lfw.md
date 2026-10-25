# Guia de leitura: base Labeled Faces in the Wild (Huang *et al.*, 2007)

> **Guia de estudo em português**, não é tradução. O relatório técnico é protegido por direitos autorais dos autores, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** HUANG, G. B.; RAMESH, M.; BERG, T.; LEARNED-MILLER, E. *Labeled Faces in the Wild*: a database for studying face recognition in unconstrained environments. Amherst: University of Massachusetts, 2007. (Technical Report 07-49). Site: [vis-www.cs.umass.edu/lfw](http://vis-www.cs.umass.edu/lfw/).
> **PDF local:** `Downloads/Referencias/huang_2007_base_lfw.pdf` · **Chave no .bib:** `huang2007lfw`

---

## Em uma frase

A LFW é uma base de fotos de rostos tiradas da internet, em condições do dia a dia, criada para estudar a **verificação facial em ambiente não controlado**: dizer se duas fotos são da mesma pessoa.

## Por que a base foi criada

As bases anteriores eram feitas em laboratório, variando um fator por vez (luz, pose, expressão). Isso ajuda a estudar cada fator, mas não reflete aplicações em que não se controla a câmera. A LFW reúne a variação "natural": pose, luz, foco, resolução, expressão, idade, gênero, etnia, acessórios, maquiagem, oclusão, fundo e qualidade da foto, tudo misturado.

## Números da base

- 13.233 imagens de 5.749 pessoas, em geral figuras públicas de notícias.
- Só 1.680 pessoas têm duas ou mais fotos; as outras 4.069 têm uma só. A média é de cerca de 2,3 fotos por pessoa.
- As fotos foram coletadas da web e os rostos localizados pelo detector de Viola-Jones; as imagens são recortadas em um formato padrão, com o rosto centralizado.
- Os rótulos de identidade foram conferidos manualmente.

## Os protocolos ("Views")

- **View 1:** para desenvolver e ajustar o algoritmo (escolher parâmetros, limiar etc.).
- **View 2:** para relatar o resultado final. São 6.000 pares (3.000 da mesma pessoa e 3.000 de pessoas diferentes), divididos em 10 partes com pessoas que não se repetem entre partes. O resultado oficial é a média de 10 rodadas de validação cruzada: treina em 9 partes, testa na décima.
- A separação entre as duas *views* existe para evitar que o pesquisador ajuste o método olhando os dados de teste.
- O relatório também discute regras de uso (por exemplo, não usar a identidade das pessoas fora dos pares fornecidos, conforme o cenário de treino escolhido).

## Limitações reconhecidas

- A base herda os vieses das fotos de notícia: mais homens, mais adultos, mais pessoas brancas, poucas crianças.
- Como os rostos foram achados por um detector, rostos muito de lado ou muito pequenos tendem a ficar de fora.
- Hoje os melhores modelos passam de 99% nela; a base ficou "fácil" e deu origem a variantes mais difíceis (CALFW, entre idades; CPLFW, entre poses).

## Ligação com o TCC

- É a base do benchmark do projeto (96 pessoas, 384 pares), já citada na Visão Geral.
- Item M1 do [documento de lacunas](../lacunas_revisao_bibliografica.md): o projeto **não** usa o protocolo View 2 de 6.000 pares, e usa o limiar padrão do DeepFace em vez de ajustá-lo em 9 partes. Por isso os números do benchmark não podem ser comparados diretamente com os 99% da literatura. Este relatório é a fonte para explicar isso na monografia.
- A falta de crianças na LFW reforça a limitação já registrada: o benchmark mede adultos, e o sistema vai reconhecer crianças.

## Perguntas para conferir a leitura

1. Qual a diferença entre a View 1 e a View 2, e por que ela importa para não "trapacear" sem querer?
2. Por que a maioria das pessoas da LFW não pode aparecer em pares positivos?
3. O que muda entre "verificação" (o que a LFW mede) e "identificação entre 20 alunos" (o que o sistema faz)?
