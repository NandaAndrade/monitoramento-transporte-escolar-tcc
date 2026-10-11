---
name: sincronizar-documentacao
description: Varre a documentação viva do repositório (anotações técnicas, resumos de leitura, relatórios de resultados, docstrings de scripts) em busca de trechos que ficaram desatualizados em relação ao estado atual do código/dados/decisões, pergunta explicitamente à usuária antes de mudar qualquer coisa, e só então atualiza o texto — preservando o estilo e a estrutura que aquele documento específico já tinha. Use sempre que o usuário pedir para "verificar se a documentação está desatualizada", "sincronizar os docs com o código", "essa anotação ainda bate com o que foi feito?", "revisar/atualizar a documentação do projeto", ou algo parecido — mesmo sem citar um arquivo específico.
---

## Objetivo

O repositório tem vários documentos "vivos" — anotações técnicas, resumos de
leitura, relatórios de resultados — que descrevem um estado do projeto no
momento em que foram escritos. Conforme o código muda, novos resultados saem
e decisões são fechadas em outro lugar, esses documentos podem ficar
desalinhados com a realidade sem que ninguém perceba, porque nada os força a
serem revisitados. O trabalho desta skill é notar esse desalinhamento antes
que alguém confie num número ou numa afirmação que não é mais verdadeira.

Duas regras não-negociáveis, porque o custo de errar aqui é maior que o de
uma atividade não fazer nada:

1. **Nunca edite um documento sem perguntar antes.** Apresente o que
   encontrou e o que pretende mudar, e espere uma resposta afirmativa clara.
   "Desatualizado" é seu diagnóstico, não uma autorização para agir.
2. **Nunca uniformize o estilo dos documentos.** Cada arquivo tem seu próprio
   registro — um é uma anotação de estudo em primeira pessoa, outro é um
   relatório técnico formal, outro é uma lista de requisitos numerada. Uma
   correção bem-feita é invisível: lê como se tivesse sido escrita pela mesma
   pessoa, no mesmo dia, que escreveu o resto do documento.

## Escopo — o que conta como "documentação viva" aqui

**Inclua:**
- Arquivos `.md` em `docs/` (e o `README.md` da raiz) que descrevem estado técnico,
  decisões ou resultados (ex.: `docs/estudo_reconhecimento_facial.md`,
  `docs/revisao_bibliografica.md`, `docs/benchmark_reconhecimento_facial.md`,
  `docs/requisitos.md`, `docs/arquitetura.md`, e qualquer novo arquivo desse tipo que apareça depois).
- O docstring/comentário de cabeçalho de scripts Python (a descrição no topo
  do arquivo, entre `"""..."""`, que explica o que o script faz, como
  instalar e como usar) — não cada comentário de linha dentro do código; isso
  é revisão de código, não documentação.

**Exclua explicitamente, e diga à usuária por quê se for perguntada:**
- `docs/relatorios_orientador/*.md` — histórico imutável gerado pela skill
  `relatorio-orientador`. Um relatório antigo não está "desatualizado", ele é
  um retrato de uma data específica; nunca reescreva um relatório já enviado.
- `monografia/historico/*.tex` — snapshots imutáveis da skill `monografia-tex`,
  pelo mesmo motivo.
- `monografia/*.tex` e `monografia/referencias.bib` — pertencem ao fluxo da skill
  `monografia-tex`, que tem seu próprio jeito de decidir onde um conteúdo
  entra e de gerar diff/citação. Se notar algo desatualizado ali, **não edite
  diretamente** — avise a usuária e sugira rodar a skill `monografia-tex` para
  aquele trecho.
- `docs/cronograma.md` — é a referência fixa de prazos combinados com o
  orientador, não um relato do estado atual do projeto. Uma atividade com
  prazo vencido não é um "erro" para esta skill corrigir; isso é assunto do
  relatório de progresso, não de sincronização de documentação.
- A proposta oficial (`docs/proposta/`) e os modelos do curso (`docs/modelos/`) — documentos formalmente entregue ao
  colegiado. Nunca editar, mesmo que algo nela pareça desatualizado.
- `.venv/`, `node_modules/`, `pesquisa/dados/`, `pesquisa/cache_deteccao/` e pastas de
  ambiente/dados brutos.
- **Qualquer arquivo com "old" no nome** (ex.: `resumo_old.md`,
  `relatorio_benchmark_old_v1.md`) — esse nome é um sinal deliberado de que o
  arquivo foi aposentado de propósito e mantido só como referência histórica.
  Trate como as pastas de histórico acima: nunca atualize, mesmo que o
  conteúdo pareça desatualizado (é esperado que esteja).

## Passo 1: localizar os candidatos

Rode um `Glob` por `docs/**/*.md` (mais o `README.md`) excluindo as pastas do
escopo acima, e liste os scripts `.py` em `pesquisa/` e os módulos em `src/presenca/`
para checar seus docstrings de cabeçalho.

Se existir um relatório recente em `docs/relatorios_orientador/` (da skill
`relatorio-orientador`), leia-o primeiro — ele frequentemente já aponta
documentos desatualizados como parte da análise de progresso (procure por algo
como "Ressalvas técnicas" ou menções a resultados/documentos defasados). Use
isso como uma lista de pistas para começar, nunca como verdade definitiva:
sempre confirme diretamente contra o código/dado atual antes de tratar algo
como desatualizado, porque o próprio relatório pode ter ficado desatualizado
entre a geração dele e agora.

## Passo 2: verificar se cada candidato ainda é verdade

Para cada documento, compare as afirmações dele com o estado atual real:

- Um script mudou de comportamento (novo parâmetro, novo modelo suportado,
  correção de bug) e o docstring/documentação que descreve como usá-lo não
  reflete isso?
- Um resultado numérico ou tabela no documento não bate com o arquivo de
  dados atual (ex.: um CSV de resultados que já tem uma linha a mais do que a
  tabela do relatório mostra)?
- Uma decisão descrita como "em aberto" já foi fechada em outro lugar mais
  recente (ex.: um requisito marcado como pendente que já tem resposta em
  outro documento)?
- Uma conclusão/recomendação foi tirada de um resultado que depois se provou
  incorreto ou incompleto (ex.: uma comparação entre modelos que ficou sem um
  dos modelos por limitação técnica já resolvida)?

Só marque algo como desatualizado quando isso realmente muda o que um leitor
entenderia — não sinalize um documento só porque é antigo, ou porque poderia
ser mais detalhado. O critério é "isso engana ou omite algo relevante hoje",
não "isso poderia estar melhor escrito".

## Passo 3: apresentar os achados e pedir permissão

Antes de tocar em qualquer arquivo, mostre à usuária, por documento:
- O que está desatualizado, especificamente (cite o trecho).
- Qual é o estado atual correto e a evidência (arquivo/dado que sustenta).
- O que você propõe mudar (não precisa ser o texto final, só a ideia).

Pergunte explicitamente se pode aplicar as mudanças — pode perguntar por
documento ou em lote ("posso atualizar estes 2 documentos assim?"), mas nunca
prossiga sem uma resposta afirmativa clara. Se a usuária aprovar só parte,
edite só essa parte.

## Passo 4: atualizar mantendo o padrão do próprio documento

Antes de editar, leia o documento inteiro (não só o trecho a corrigir) para
internalizar como ele é escrito: estrutura de seções, se usa tabela ou prosa,
se é redigido em primeira pessoa ou em tom de relatório técnico, o nível de
formalidade, convenções próprias (ex.: como ele cita fontes, como nomeia
arquivos). A edição deve parecer ter sido escrita pela mesma "voz" do resto
do documento — edite só o que precisa mudar, sem reescrever ou reformatar
partes que já estavam corretas.

O repositório tem controle de versão (`git`). Depois de editar, rode
`git diff -- <arquivo>` para conferir exatamente o que mudou antes de mostrar
o resultado à usuária — é uma forma mais confiável de revisar a própria
edição do que reler o arquivo inteiro de novo. Não faça commit automaticamente;
isso fica a critério da usuária.

## Passo 5: fechar o ciclo

Mostre o diff de cada arquivo alterado e um resumo de 1-2 frases por arquivo
do que mudou e por quê. Se algum achado do Passo 2 não foi aprovado para
edição, deixe registrado na conversa que ficou pendente, para não se perder.
