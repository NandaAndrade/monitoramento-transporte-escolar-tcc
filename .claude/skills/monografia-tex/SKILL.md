---
name: monografia-tex
description: Incorpora um novo pedaço de conteúdo (resultado, decisão, resumo de leitura, texto já escrito pela aluna) na monografia de TCC em LaTeX (monografia/monografia_tcc1.tex), identificando sozinha em qual capítulo/seção aquilo pertence, escrevendo o trecho em prosa acadêmica ABNT, atualizando referencias.bib quando houver citação, e mostrando um diff do que mudou. Use sempre que o usuário disser algo como "inclui isso na monografia", "escreve essa parte pro TCC", "adiciona esse resultado no texto", "isso já pode entrar na revisão bibliográfica/introdução/metodologia", ou colar/descrever um conteúdo e pedir para "colocar no TCC" — mesmo sem mencionar o nome do arquivo .tex ou a palavra "monografia" explicitamente.
---

## Objetivo

A aluna vai, ao longo do projeto, trazer pedaços de conteúdo em momentos
diferentes — um resultado de benchmark, uma decisão de arquitetura, um resumo
de artigos lidos, um requisito levantado, um parágrafo que ela mesma já
escreveu. O trabalho desta skill é pegar cada pedaço novo e integrá-lo ao
texto único e coerente de `monografia_tcc1.tex`, no lugar certo, escrito no
registro de uma monografia (não como nota solta), sem duplicar o que já existe
e sem perder o que já estava escrito.

O entregável final que a aluna vai compilar no Overleaf é sempre
`monografia/monografia_tcc1.tex` (mais `monografia/referencias.bib` e a pasta `monografia/imagens/` com as
imagens da capa — os três precisam estar juntos no mesmo projeto do Overleaf,
já que o pedido original de "um arquivo .tex" não inclui uma forma prática de
embutir imagens e uma base de citações ABNT dentro do próprio `.tex`; isso é
uma limitação do LaTeX, não uma escolha arbitrária desta skill). Lembre a
usuária disso sempre que ela for compilar pela primeira vez ou copiar os
arquivos para um projeto novo.

## Passo 1: ler o estado atual antes de escrever qualquer coisa

Leia `monografia/monografia_tcc1.tex` e `monografia/referencias.bib` inteiros a cada execução — nunca
edite a partir de uma versão lembrada de uma execução anterior, porque a
aluna pode ter editado o arquivo diretamente no Overleaf entre uma execução e
outra.

O `.tex` tem 5 capítulos textuais fixos (definidos pelo escopo formal do
TCC I, atividade 1.5 da proposta): **Introdução**, **Revisão Bibliográfica**,
**Metodologia**, **Avaliação de Impactos Socioeconômicos, Legais e de
Humanidades**, e **Cronograma do TCC II**. Um capítulo que ainda não foi
escrito tem um comentário `% TODO(monografia-tex): ...` explicando o que se
espera dele — leia esse comentário antes de escrever, ele é a especificação
do que pertence ali.

Não crie um sexto capítulo ou renomeie os existentes só porque um conteúdo
novo não parece caber perfeitamente em nenhum — praticamente tudo que a aluna
vai trazer se encaixa em um desses cinco quando você pensa no *papel* do
conteúdo (é fundamentação teórica? é uma escolha de projeto e seu porquê? é
uma restrição legal/social?), não no vocabulário literal do pedido. Se depois
de pensar assim ainda não houver encaixe razoável, pare e pergunte à usuária
em vez de forçar ou inventar uma seção nova.

## Passo 2: decidir onde o conteúdo novo entra

Use o *conteúdo real*, não o nome do arquivo/mensagem, para decidir o
capítulo — a mesma fonte pode alimentar mais de um capítulo ao mesmo tempo,
em partes diferentes. Alguns exemplos concretos já vistos neste projeto, para
calibrar o julgamento (não são regras fixas, são exemplos de como pensar):

- Uma comparação de algoritmos de reconhecimento facial com base em artigos
  e documentação de bibliotecas → **Revisão Bibliográfica** (é fundamentação
  teórica, precisa de citações).
- O resultado empírico de rodar esses algoritmos contra um dataset e escolher
  os 2 melhores → também **Revisão Bibliográfica** na maior parte (é a
  continuação natural da fundamentação com dados próprios), mas o *porquê* de
  ter escolhido aquele dataset/metodologia de teste (ex.: por que não usar
  fotos reais de alunos) pertence à **Metodologia** ou à **Avaliação de
  Impactos** (restrição de LGPD).
- Um levantamento de requisitos funcionais/não funcionais → majoritariamente
  **Introdução** (escopo do problema) e **Metodologia** (como cada requisito
  será verificado), não uma lista de RF/RNF colada sem adaptação — o
  documento de requisitos do repositório pode ser mais técnico/telegráfico do
  que o registro esperado numa monografia; reescreva em prosa, você pode
  manter uma tabela quando ela for genuinamente mais clara em prosa (ex.: a
  tabela comparativa dos 10 algoritmos), mas não copie blocos de markdown
  crus para dentro do `.tex`.
- Uma decisão de hardware (Raspberry Pi vs. ESP32) com a justificativa técnica
  → **Metodologia** (é projeto arquitetural) — mas se a decisão ainda estiver
  em aberto, registre isso como está: um TODO/parágrafo dizendo que a análise
  de trade-off está em andamento, não uma conclusão que ainda não foi tomada.
- Cronograma de atividades do TCC II → **Cronograma do TCC II**, óbvio pelo
  nome, mas vale conferir se `docs/cronograma.md` já tem esse detalhamento
  antes de inventar datas.

Se o conteúdo novo contradiz ou substitui algo já escrito (ex.: o benchmark
tinha uma conclusão preliminar que depois mudou), edite o texto existente em
vez de simplesmente acrescentar um parágrafo novo dizendo o contrário logo
depois — a monografia final deve ler como um texto escrito de uma vez, não
como um histórico de idas e vindas.

## Passo 3: escrever em prosa acadêmica ABNT

- Terceira pessoa ou voz passiva, tempo verbal consistente com o resto do
  capítulo (geralmente presente ou futuro do presente, já que TCC I descreve
  o que *será* feito no TCC II além do que já foi levantado).
- Sem gírias, sem primeira pessoa ("eu decidi"), sem tom de conversa/anotação
  de estudo — transforme "testei 10 modelos e o ArcFace ganhou" em algo como
  "foram avaliados dez algoritmos de reconhecimento facial [...], dos quais o
  ArcFace apresentou a maior acurácia [...]".
- Toda afirmação que vem da literatura (um algoritmo, uma técnica, um dado de
  outro trabalho) precisa de `\cite{chave}`, com a entrada correspondente
  adicionada a `referencias.bib`. **Nunca invente uma referência** — se a
  aluna não informou autor/ano/título da fonte, não crie uma entrada bibtex
  fictícia para preencher a lacuna; em vez disso, deixe um comentário
  `% TODO: citar fonte de <afirmação>` no `.tex` e avise isso claramente no
  resumo que você dá pra ela no final. Uma citação fabricada é um problema de
  integridade acadêmica sério, muito pior do que uma lacuna visível.
- Resultados numéricos/tabelas (ex.: comparação de modelos) podem virar uma
  tabela LaTeX (`table`/`tabular`) com legenda (`\caption`) — isso é mais
  apropriado numa monografia do que descrever cada número em texto corrido.
- Não escreva o Resumo (abstract em português) até que Introdução, Revisão
  Bibliográfica e Metodologia já tenham conteúdo real — resumo se escreve por
  último, resumindo o que já existe. Se pedirem para "atualizar o resumo"
  antes disso, avise que ainda é cedo e pergunte se querem prosseguir mesmo
  assim.

## Passo 4: aplicar a edição e gerar o diff

Antes de editar `monografia/monografia_tcc1.tex`, copie o conteúdo atual para
`monografia/historico/monografia_tcc1_AAAA-MM-DD_HHhMM.tex` (crie a pasta se
não existir — o carimbo de hora, não só a data, é necessário porque pode haver
mais de uma edição no mesmo dia). Isso cumpre o mesmo papel que o `git diff`
cumpriria se o repositório tivesse controle de versão: dá um "antes" real
para comparar.

Depois de salvar a nova versão de `monografia/monografia_tcc1.tex`, gere um diff unificado
entre a cópia em `historico/` (antes) e o arquivo atualizado (depois). Rode:

```python
import difflib

with open("monografia/historico/<snapshot_usado>.tex", encoding="utf-8") as f:
    antes = f.readlines()
with open("monografia/monografia_tcc1.tex", encoding="utf-8") as f:
    depois = f.readlines()

diff = difflib.unified_diff(antes, depois, fromfile="antes", tofile="depois", lineterm="")
print("\n".join(diff))
```

Mostre esse diff para a usuária na conversa (não precisa salvá-lo em arquivo
à parte, a menos que fique muito longo — nesse caso, salve como
`monografia/historico/diff_AAAA-MM-DD_HHhMM.txt` e aponte o caminho). Se
`referencias.bib` também mudou, gere e mostre o diff dele separadamente pelo
mesmo método.

## Passo 5: fechar o ciclo

Ao terminar, diga à usuária, em poucas frases:
- Em qual(is) capítulo(s) o conteúdo entrou e por quê (isso ajuda a validar
  se a classificação fez sentido).
- Se alguma citação ficou marcada como `% TODO: citar fonte` — liste
  explicitamente, para que ela não passe despercebida quando for pro Overleaf.
- Lembre que `monografia_tcc1.tex`, `referencias.bib` e `imagens/` (na
  primeira vez) precisam estar juntos no projeto do Overleaf para compilar.
