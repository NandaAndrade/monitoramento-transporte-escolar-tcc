---
name: relatorio-orientador
description: Gera um relatório de progresso do TCC para enviar ao orientador (Janier Arias García) e coorientador (Frederico Gualberto Ferreira Coelho), varrendo o repositório para levantar o que já existe de documentação, implementação e decisões tomadas, e comparando isso com o cronograma oficial da proposta de TCC1. Use sempre que o usuário pedir para "atualizar o orientador", "mandar um status pro professor", "fazer um relatório de progresso/andamento do TCC", "resumir o que já foi feito", "preparar um update" ou algo parecido — mesmo que a pessoa não use as palavras exatas "cronograma" ou "relatório".
---

## Objetivo

Produzir um relatório curto e objetivo, em português, que a aluna possa mandar por
e-mail para o orientador e coorientador mostrando: o que foi feito desde o último
relatório (ou desde o início, se for o primeiro), como isso se compara ao cronograma
oficial do TCC1, e o que precisa da atenção/decisão deles.

O valor desse relatório não é só "informar" — é permitir que o orientador identifique
rapidamente duas coisas distintas: (1) se o projeto está no prazo, e (2) se o que foi
trabalhado e decidido tecnicamente desde o último relatório está na linha esperada,
independente do prazo. Um item pode estar no prazo e mesmo assim seguir numa direção
técnica que o orientador não validaria (ex.: uma escolha de algoritmo, um critério de
teste, uma interpretação de resultado) — é exatamente esse tipo de desvio que o
orientador só consegue pegar a tempo se o relatório expuser o raciocínio técnico, não
só o status da tarefa. Por isso, priorize clareza e honestidade sobre o estado real
(inclusive atrasos) e sobre o conteúdo técnico do que foi feito, em vez de deixar tudo
parecer "em dia" ou reduzir o relatório a uma lista de tarefas concluídas.

Este repositório não tem controle de versão (`git`) inicializado, então não há
histórico de commits para consultar — a evidência de progresso vem do conteúdo e das
datas de modificação dos arquivos, e de relatórios anteriores gerados por esta mesma
skill. Se em algum momento o repositório for inicializado com git, prefira `git log`
como fonte de datas por ser mais confiável que o timestamp do sistema de arquivos.

## Passo 1: ler o cronograma oficial

**`Cronograma_Oficial.md`, na raiz do repositório, é sempre a única fonte do
cronograma para este relatório.** Releia o arquivo inteiro a cada execução — nunca
reaproveite uma versão memorizada de uma execução anterior, porque a aluna edita
esse arquivo diretamente quando um prazo muda ou uma atividade nova é combinada
com o orientador. Ele já teve datas atualizadas no meio do projeto antes, então
tratá-lo como fixo geraria relatórios desatualizados sem que ninguém percebesse.

Use as duas tabelas de `Cronograma_Oficial.md` (atividades práticas com data exata,
e entregas de documentação) como a lista real de itens a avaliar no relatório — não
a tabela mensal do PDF da proposta, que é mais grosseira (só mês, sem dia) e serve
aqui apenas como contexto textual de fundo para entender o que cada "Atividade X.Y"
formal significa, caso o Cronograma_Oficial.md se refira a ela de forma abreviada.

Se `Cronograma_Oficial.md` não existir (por exemplo, foi renomeado ou apagado), não
tente reconstruir o cronograma sozinho a partir do PDF/docx — pare e avise a usuária
que o arquivo esperado não foi encontrado, e pergunte onde está o cronograma vigente
antes de continuar.

## Passo 2: inventariar o repositório

Percorra o repositório (ignore `.venv/`, `node_modules/`, e outras pastas de
dependências/ambiente virtual — elas não são trabalho da aluna) e classifique o que
encontrar em três baldes:

1. **Documentação** — `.md`, `.docx`, `.pdf`, anotações de reunião, resumos de
   pesquisa (ex.: `resumo_reconhecimento_facial_tcc.md`).
2. **Implementação** — código-fonte, scripts, notebooks, configs, datasets gerados.
3. **Decisões tomadas** — não costumam ter um arquivo dedicado, então procure por
   trechos de texto que indiquem uma escolha feita e sua justificativa (padrões como
   "decidido", "optou-se por", "escolha de", "trade-off", "conclusão preliminar",
   comentários de código explicando por que algo foi feito de um jeito). Uma decisão
   vale mais no relatório quando vem acompanhada do *porquê* — extraia isso, não só
   o "o quê".

Para cada item relevante, anote do que se trata e, quando possível, a data de
modificação do arquivo (`Get-ChildItem` / `os.stat`) como pista aproximada de quando
foi produzido. Deixe claro para si mesmo que isso é uma aproximação, não um fato
confirmado — o timestamp do arquivo pode não refletir quando o trabalho realmente
aconteceu (por exemplo, se um arquivo foi copiado ou tocado sem mudança de conteúdo).

Se existir um relatório anterior gerado por esta skill (veja Passo 5 — pasta
`relatorios/`), leia o mais recente primeiro. Ele já tem o inventário e a avaliação de
status da última vez; seu trabalho agora é identificar **o que mudou** desde então,
não reconstruir tudo do zero. Isso torna relatórios sucessivos mais curtos e mais
úteis (um orientador não precisa reler o que já leu da última vez).

## Passo 3: comparar com o cronograma e avaliar o status

Para cada linha das tabelas de `Cronograma_Oficial.md` (atividades práticas e
entregas de documentação), determine:

- **Status**: Concluída / Em andamento / Não iniciada / Adiantada (trabalho de uma
  atividade futura já começou).
- **Evidência**: qual arquivo(s) sustentam essa avaliação.
- **Posição no tempo**: compare a data prevista (dia/mês/ano exatos, não só o mês)
  com a data atual. Um item cuja data já passou e que não tem evidência de conclusão
  está **atrasado** — diga isso explicitamente, sem suavizar. Um item cuja data ainda
  não chegou mas já tem trabalho encaminhado está **adiantado** — isso também é
  informação valiosa (mostra iniciativa, mas pode também sinalizar que a aluna está
  pulando etapas, como testar algoritmos antes de fechar o levantamento de requisitos).
- **Alinhamento técnico**: independente do status de prazo, avalie se o conteúdo do
  que foi feito faz sentido tecnicamente e está na direção esperada para aquela
  atividade — não só se a caixinha foi marcada como concluída. Por exemplo: a escolha
  de um algoritmo baseada em uma metodologia de teste falha (dataset pequeno demais,
  detector mal configurado, threshold não calibrado) é uma atividade "concluída" no
  cronograma mas tecnicamente frágil, e isso é mais importante para o orientador saber
  do que o status por si só. Sempre que notar algo assim — uma limitação metodológica,
  uma decisão tomada sem base suficiente, um resultado que contraria a expectativa da
  literatura sem explicação — registre isso mesmo que não exista uma linha própria no
  cronograma para "qualidade da atividade": isso é o tipo de sinal que só aparece
  quando alguém lê o conteúdo, não a data de entrega. Cada achado desses vira **um item
  da seção "Ressalvas técnicas"** do relatório (Passo 4) — não um parágrafo solto nem um
  título de seção inventado na hora; a seção já tem nome e lugar fixos no esqueleto.

Não force uma correspondência perfeita entre arquivo e atividade só pelo nome — julgue
pelo conteúdo. Por exemplo, um script de benchmark de reconhecimento facial não é
"Atividade 1.2" só porque parece bibliografia; ele pode sustentar tanto a Atividade 1.2
(revisão bibliográfica, se comparar algoritmos da literatura) quanto dar insumo
concreto para a Atividade 1.3 (trade-offs de arquitetura), dependendo do que o
conteúdo realmente discute.

## Passo 4: escrever o relatório

Use exatamente esta estrutura (adapte o texto, não o esqueleto):

```markdown
# Relatório de Progresso — TCC [título curto do projeto]

**Data:** [data de hoje]
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García — **Coorientador:** Frederico Gualberto Ferreira Coelho
**Período coberto:** [desde o último relatório em DD/MM/AAAA, ou "início do projeto"]

## Resumo executivo
[3-5 linhas: o essencial que o orientador precisa saber antes de ler o resto]

## Progresso — atividades práticas

| Data prevista | Atividade | Status | Evidência |
|---|---|---|---|
| [DD/MM/AAAA] | [texto da linha em Cronograma_Oficial.md] | ... | ... |

## Progresso — entregas de documentação

| Data prevista | Entrega | Status | Evidência |
|---|---|---|---|
| [DD/MM/AAAA] | [texto da linha em Cronograma_Oficial.md] | ... | ... |

## Ressalvas técnicas
[Uma lista de achados objetivos sobre a qualidade/direção técnica do trabalho, independente
de prazo — ver "Alinhamento técnico" no Passo 3. Cada item: 1-2 frases, fato + por que
importa, sem repetir o que a tabela de progresso já disse. Se não houver nenhuma ressalva
neste período, escreva uma linha dizendo isso em vez de omitir a seção.]

## Decisões tomadas
[Cada decisão com o porquê. Se não houve nenhuma decisão nova desde o último relatório, diga isso em uma linha em vez de omitir a seção.]

## Pendências e próximos passos
[O que falta, priorizado. Se um item já foi explicado em "Ressalvas técnicas", cite-o em
poucas palavras e não repita a explicação (ex.: "Repetir benchmark com detector mais
robusto (ver Ressalvas técnicas)").]

## Pontos que precisam de decisão ou orientação
[Perguntas concretas para o orientador/coorientador — isso é frequentemente a parte mais útil do relatório]
```

Regras fixas de formato:

- **Os títulos das seções são exatamente os do esqueleto acima — nunca invente um título
  novo nem acrescente um complemento entre parênteses** (ex.: nunca escrever "Ressalvas
  técnicas (alinhamento, não só prazo)"). Se algo precisa de explicação, essa explicação
  entra no corpo da seção, não no título — um status report não carrega comentário
  editorial no cabeçalho.
- **Cada fato aparece uma única vez, na seção a que pertence.** Status e evidência de prazo
  vão só nas tabelas; qualidade/direção técnica só em "Ressalvas técnicas"; escolha
  justificada só em "Decisões tomadas"; ação futura só em "Pendências e próximos passos".
  Ao escrever cada seção, verifique se a frase que está prestes a escrever já apareceu
  (ainda que com outras palavras) em uma seção anterior — se sim, corte ou substitua por
  uma referência curta em vez de reescrever a explicação.

Escreva em tom objetivo e profissional, como quem está reportando para um professor —
evite linguagem excessivamente informal, mas também não precisa ser rebuscado. Prefira
frases diretas a parágrafos longos. Se alguma seção não tiver conteúdo real (ex.: sem
decisões novas, sem pendências urgentes), diga isso explicitamente em vez de inventar
conteúdo para preencher.

Não mencione no corpo do relatório em que dia/momento específico algo foi feito (ex.:
"no mesmo dia", "hoje mais cedo", "em 16/09") — o campo **Período coberto** no
cabeçalho já contextualiza a janela de tempo do relatório inteiro, então repetir a
data dentro do texto não agrega informação para o orientador e soa como um detalhe de
processo interno da aluna, não como parte do conteúdo do projeto. Descreva o que foi
feito no período coberto, sem granularidade de quando dentro dele — a granularidade
por dia só importa nas tabelas de progresso, onde a data prevista de cada item vem do
cronograma.

## Passo 5: salvar o relatório

Salve o arquivo em `relatorios/relatorio_AAAA-MM-DD.md` (crie a pasta se não existir).
Guardar os relatórios com data no próprio repositório cria, com o tempo, um histórico
de progresso que compensa a ausência de `git log` — releia relatórios antigos sempre
que precisar reconstruir "o que já foi dito ao orientador até aqui".

Ao terminar, avise a usuária onde o arquivo foi salvo e ofereça um resumo de 2-3
frases do conteúdo, para que ela possa decidir rapidamente se quer revisar algo antes
de enviar.
