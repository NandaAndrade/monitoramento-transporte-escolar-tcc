# Guia de Estudo — Fundamentos Teóricos do TCC

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Para quem é:** Fernanda, ponto de partida "conhecimento superficial" (diagnóstico feito em 2026-10-05)
**Objetivo:** conseguir acompanhar, explicar com as próprias palavras e defender na banca tudo o que já existe no repositório: [requisitos](requisitos.md), [anotações da revisão](revisao_bibliografica.md), [resumo de reconhecimento facial](estudo_reconhecimento_facial.md) e [relatório do benchmark](benchmark_reconhecimento_facial.md).

> **Diagnóstico que orientou este guia**
> - Conceitos de IA (detecção × reconhecimento, embedding, precisão/recall): **começar do zero**
> - Redes neurais / deep learning: **quase nenhum contato**
> - Hardware (Raspberry Pi × ESP32): **começar do zero**
> - MQTT: **já conhece** (publish/subscribe), então aqui ele só aparece ligado ao projeto
> - Python: **básico**, então o código é explicado trecho a trecho
>
> **Como ler:** na ordem. Cada parte usa a anterior. As caixas "📌 Na banca" mostram a frase-resumo que você deveria conseguir dizer de memória. No fim há perguntas de autoavaliação (incluindo as que você respondeu "não sei" no diagnóstico).

---

## Sumário

1. [O projeto em uma página](#1-o-projeto-em-uma-página)
2. [O mínimo de IA que você precisa](#2-o-mínimo-de-ia-que-você-precisa)
3. [Etapa 1: detecção facial](#3-etapa-1-detecção-facial)
4. [Etapa 2: reconhecimento facial e embeddings](#4-etapa-2-reconhecimento-facial-e-embeddings)
5. [Como esses modelos aprendem (perdas)](#5-como-esses-modelos-aprendem)
6. [Os 10 modelos do benchmark](#6-os-10-modelos-do-benchmark)
7. [Métricas: acurácia, precisão, recall e F1](#7-métricas-acurácia-precisão-recall-e-f1)
8. [Lendo o benchmark do seu TCC](#8-lendo-o-benchmark-do-seu-tcc)
9. [Hardware embarcado e edge computing](#9-hardware-embarcado-e-edge-computing)
10. [Comunicação: MQTT no contexto do projeto](#10-comunicação-mqtt-no-contexto-do-projeto)
11. [Reconhecimento de voz](#11-reconhecimento-de-voz)
12. [LGPD e dados biométricos](#12-lgpd-e-dados-biométricos)
13. [Glossário](#13-glossário)
14. [Autoavaliação](#14-autoavaliação)
15. [O que estudar depois](#15-o-que-estudar-depois)

---

## 1. O projeto em uma página

**Problema:** no transporte escolar rural, ninguém sabe com segurança quais alunos embarcaram e desembarcaram, nem onde.

**Solução proposta:** um dispositivo dentro do ônibus (câmera + microfone + um pequeno computador) que:

1. vê o rosto (e/ou ouve a voz) do aluno ao embarcar ou desembarcar;
2. descobre **qual aluno cadastrado** é aquele;
3. registra o evento ("aluno X embarcou às 7h14 no ponto Y");
4. envia o evento para o sistema **TRANSCOLAR RURAL** pela rede móvel (MQTT), ou guarda numa fila se estiver sem sinal.

O "cérebro" da etapa 2 é o que você está estudando agora. O caminho completo de uma imagem até virar um registro é este:

```
 câmera                         dispositivo no ônibus                                 nuvem
┌──────┐   quadro   ┌───────────┐  recorte   ┌──────────────┐  vetor  ┌──────────────┐  evento  ┌─────────────┐
│ vídeo│──────────▶│ DETECÇÃO  │──do rosto─▶│RECONHECIMENTO│────────▶│ COMPARAÇÃO   │─────────▶│ TRANSCOLAR  │
└──────┘           │ "onde há  │           │ "transforma  │ (embed- │ com os alunos│  (MQTT)  │   RURAL     │
                   │  rosto?"  │           │  o rosto em  │  ding)  │ cadastrados  │          └─────────────┘
                   │ YuNet,    │           │  números"    │         │ "é a Ana?    │
                   │ RetinaFace│           │ ArcFace,SFace│         │  é o João?"  │
                   └───────────┘           └──────────────┘         └──────────────┘
```

Guarde esta figura: **quase todo o resto do guia explica uma caixa dela.**

> 📌 **Na banca:** "O sistema é um pipeline de duas etapas de visão computacional, detecção e reconhecimento, rodando na borda, ou seja, no próprio ônibus. Ele envia só o evento de presença, nunca a imagem."

---

## 2. O mínimo de IA que você precisa

### 2.1 Para o computador, uma imagem é uma tabela de números

Uma foto colorida de 250×250 pixels é, para o computador, uma tabela de 250 linhas × 250 colunas × 3 canais (vermelho, verde, azul), com cada valor entre 0 e 255. Ou seja, são **187.500 números**. Comparar duas fotos "número a número" não funciona: a mesma pessoa com outra luz ou outro ângulo gera números completamente diferentes.

O que queremos é um jeito de transformar a foto em algo que **mude pouco quando é a mesma pessoa** e **mude muito quando é outra pessoa**. É isso que os modelos de IA fazem.

### 2.2 O que é um "modelo"

Um **modelo** é uma função matemática com muitos "botões de ajuste", os **parâmetros** (ou pesos). Ele recebe uma entrada (a imagem) e produz uma saída (por exemplo, uma lista de números). Os valores dos botões decidem o que o modelo faz.

- **Treino:** mostrar milhões de exemplos ao modelo e ajustar os botões aos poucos para ele errar menos. É caro, exige GPU e leva dias. **Você não vai treinar modelos de rosto no TCC.**
- **Inferência:** usar o modelo já treinado, com os botões congelados, para processar uma entrada nova. É isso que o Raspberry Pi vai fazer no ônibus.

Os 10 modelos do seu benchmark são **pré-treinados**: alguém (Google, Facebook, Oxford, etc.) já treinou com milhões de fotos de rostos, e você só os usa. Por isso o "tamanho do modelo" (5 MB, 130 MB, 580 MB) é basicamente **a quantidade de botões salvos em disco**.

### 2.3 Rede neural, em uma imagem mental

Uma **rede neural** é um tipo específico de modelo, montado como uma sequência de **camadas**. Cada camada recebe números, faz contas simples (multiplica pelos pesos, soma, aplica uma função) e passa o resultado adiante.

- As primeiras camadas aprendem sozinhas a detectar coisas simples: bordas, cantos, manchas de cor.
- As camadas do meio combinam isso em partes: olho, canto da boca, contorno do nariz.
- As últimas camadas combinam as partes em algo abstrato: "o jeito do rosto desta pessoa".

**Deep learning** é só "rede neural com muitas camadas" (profunda).

### 2.4 CNN: a rede neural feita para imagens

Uma **CNN** (*Convolutional Neural Network*, rede neural convolucional) é a família usada em praticamente todos os modelos deste TCC. A ideia central é a **convolução**: uma pequena "lupa" (um filtro de, por exemplo, 3×3 pixels) desliza pela imagem inteira procurando um padrão. Um filtro pode aprender a achar bordas verticais, outro, bordas horizontais, e assim por diante.

Por que isso é bom para imagens: um olho é um olho em qualquer lugar da foto, então faz sentido usar **o mesmo filtro** em todas as posições. Isso economiza muitos parâmetros.

Nomes que você vai ver e que são **arquiteturas de CNN** (o "formato" da rede):

| Nome | O que lembrar |
|---|---|
| **ResNet** | Rede profunda e precisa; usada por ArcFace, Dlib e RetinaFace (versão grande) |
| **MobileNet / MobileFaceNet** | Versões enxutas, pensadas para celular e dispositivos pequenos |
| **GhostNet** | Outra arquitetura enxuta, que gera parte das contas "de graça" a partir de outras (base do GhostFaceNet) |

A arquitetura enxuta (no inglês, *backbone*) é muitas vezes o que separa um modelo de 130 MB de outro de 4 MB **com o mesmo método de treino**. Por isso o seu resumo diz que o ArcFace "pesado" tem 130 MB, mas existe ArcFace com backbone MobileFaceNet de cerca de 4 MB.

> 📌 **Na banca:** "Os modelos são CNNs pré-treinadas. No dispositivo só fazemos inferência, então o que importa para o hardware é o tamanho do modelo e o tempo de inferência, não o custo de treino."

---

## 3. Etapa 1: detecção facial

### 3.1 O que é

**Detecção** responde a: *"existe um rosto nesta imagem? Onde?"*. Ela **não sabe de quem é** o rosto. A saída é:

- uma **caixa delimitadora** (*bounding box*): o retângulo (x, y, largura, altura) ao redor do rosto;
- muitas vezes, **5 pontos de referência** (*landmarks*): os dois olhos, a ponta do nariz e os dois cantos da boca;
- uma **confiança** (ex.: 0,97 = "tenho 97% de certeza de que é um rosto").

### 3.2 Por que essa etapa importa tanto

Os modelos de reconhecimento esperam receber **só o rosto, recortado e alinhado** (olhos na horizontal, em posição padrão). Os landmarks servem justamente para **alinhar**: gira-se a imagem até os olhos ficarem nivelados.

Se a detecção falha, por exemplo cortando metade do rosto ou não achando rosto nenhum, o reconhecimento recebe lixo e **erra, mesmo sendo um ótimo modelo**. Isso explica parte dos resultados ruins do seu benchmark (ver [seção 8.3](#83-por-que-alguns-modelos-tiveram-recall-tão-baixo)).

### 3.3 Os detectores citados no trabalho

| Detector | Ano | Ideia | Para o projeto |
|---|---|---|---|
| **Haar Cascade** (Viola–Jones) | 2001 | Método clássico, sem deep learning: procura padrões de claro/escuro (ex.: região dos olhos mais escura que a testa). Muito rápido. | É o `detector_backend="opencv"` usado no benchmark. Leve, mas **fraco** com rosto inclinado, de lado ou com pouca luz. |
| **MTCNN** | 2016 | Três CNNs pequenas em cascata | Intermediário; citado como alternativa no script |
| **RetinaFace** | 2019 | CNN grande e multitarefa, focada em **precisão** | Robusto em rostos pequenos, ocluídos ou de lado; mais pesado. Há relatos de rodar no Hailo. |
| **YuNet** | 2021–22 | CNN minúscula (~100 KB), focada em **velocidade** | Já vem dentro do OpenCV (`cv2.FaceDetectorYN`); ótimo encaixe para o Pi |

> 📌 **Na banca:** "Detecção localiza o rosto e fornece landmarks para alinhamento; reconhecimento identifica a pessoa. A qualidade final depende das duas etapas. No benchmark usamos o detector mais leve (Haar), o que provavelmente penalizou alguns modelos."

---

## 4. Etapa 2: reconhecimento facial e embeddings

Esta é a ideia mais importante do TCC. Se entender só uma seção, que seja esta.

### 4.1 Embedding: a "impressão digital numérica" do rosto

Um modelo como ArcFace **não devolve o nome da pessoa**. Ele recebe o recorte do rosto e devolve um **vetor**, uma lista de números de tamanho fixo (512 números no ArcFace, 128 no SFace). Esse vetor se chama **embedding** (ou *template* biométrico).

O modelo foi treinado para que:

- fotos **da mesma pessoa** gerem vetores **próximos**;
- fotos **de pessoas diferentes** gerem vetores **distantes**.

Imagine cada vetor como um ponto num mapa (com 512 dimensões em vez de 2, mas a intuição é a mesma):

```
           ● Ana (foto 1)
          ● Ana (foto 2, outra luz)         ▲ João (foto 1)
         ● Ana (foto 3, de lado)          ▲ João (foto 2)

                       ■ Maria (foto 1)
                        ■ Maria (foto 2)
```

O modelo **nunca precisou ver a Ana durante o treino**. Ele aprendeu "o que faz rostos diferirem" em geral, e isso funciona para gente nova. É por isso que dá para usar um modelo pronto com os seus alunos.

### 4.2 Distância e limiar (threshold)

Para decidir se dois rostos são da mesma pessoa:

1. gera-se o embedding de cada um;
2. mede-se a **distância** entre os dois vetores;
3. compara-se com um **limiar**: abaixo dele, "mesma pessoa"; acima, "pessoas diferentes".

A distância mais usada é a **distância cosseno**, que mede o ângulo entre os dois vetores (0 = mesma direção, ou seja, muito parecidos). Em fórmula, sendo *a* e *b* os vetores:

```
similaridade_cosseno = (a · b) / (|a| × |b|)        → entre -1 e 1
distância_cosseno     = 1 − similaridade_cosseno    → 0 = idênticos
```

Você não precisa calcular isso à mão. Basta saber que **é um número que diz o quão diferentes os rostos são**, e que **o limiar é uma escolha de projeto**:

- limiar **baixo** (exigente): só aceita quando os rostos são muito parecidos. Quase nunca confunde pessoas, mas às vezes não reconhece a própria pessoa;
- limiar **alto** (tolerante): reconhece mais, mas arrisca confundir pessoas.

A biblioteca DeepFace usa um limiar padrão diferente para cada modelo. **Isso vai ser crucial para entender o seu benchmark.**

### 4.3 Verificação (1:1) × identificação (1:N)

| | Verificação (1:1) | Identificação (1:N) |
|---|---|---|
| Pergunta | "Estas duas fotos são da mesma pessoa?" | "De qual das N pessoas cadastradas é este rosto?" |
| Exemplo | Desbloquear o celular | **Embarque no ônibus** |
| Como faz | 1 comparação + limiar | compara com os N cadastrados, pega o mais próximo e checa o limiar |

**O benchmark mediu verificação** (`DeepFace.verify`, pares de fotos). **O sistema real faz identificação**: o rosto que entra é comparado aos ~20 alunos daquele ônibus (RNF-01). As duas coisas estão ligadas, porque identificação nada mais é do que várias verificações, mas os números não são iguais. Vale citar isso como limitação na monografia.

O "e se não bater com ninguém?" também importa: se a menor distância ainda está acima do limiar, o sistema deve dizer "desconhecido" e gerar um alerta (RF-04), em vez de forçar o aluno mais parecido.

### 4.4 Cadastro (enrollment)

Antes de usar, cada aluno precisa ser **cadastrado**: tira-se uma ou mais fotos de referência, gera-se o embedding e **guarda-se o embedding**. A foto pode ser descartada. No embarque, só se compara o embedding novo com os guardados.

Isso conversa diretamente com o RF-05 e o RNF-07 (não guardar imagem bruta) e com a LGPD (seção 12).

> 📌 **Na banca:** "O modelo de reconhecimento mapeia cada rosto em um vetor de características, o embedding. A identificação compara o embedding capturado com os embeddings cadastrados via distância cosseno e um limiar de decisão. No cadastro guardamos só o embedding, não a foto."

---

## 5. Como esses modelos aprendem

Você não vai treinar, mas a banca pode perguntar **por que ArcFace é melhor que FaceNet**, e a resposta está no **jeito de treinar**, a chamada **função de perda** (*loss*): a nota que diz ao modelo o quanto ele errou, para ele ajustar os pesos.

| Abordagem | Modelo exemplo | Intuição |
|---|---|---|
| **Classificação comum** (softmax) | DeepFace (Facebook), DeepID, VGG-Face | Treina a rede para dizer "esta foto é a pessoa nº 3.817 do dataset". Depois, joga-se fora a última camada e usa-se a penúltima como embedding. Funciona, mas os grupos de cada pessoa ficam "frouxos" no mapa. |
| **Triplet loss** | FaceNet (Google, 2015) | Mostra três fotos: âncora (Ana), positiva (outra da Ana) e negativa (João). Penaliza se a Ana-âncora estiver mais perto do João que da outra Ana. Aprende a distância diretamente. |
| **Margem angular** | **ArcFace** (2019), SFace | Coloca os embeddings numa esfera e exige que cada pessoa fique a um **ângulo mínimo de folga (margem)** das outras. Os grupos ficam mais compactos e mais separados. Por isso ArcFace é referência em acurácia. |

**Imagem mental da margem angular:** na classificação comum basta a Ana estar do lado certo da fronteira. No ArcFace ela precisa estar do lado certo **e longe da fronteira**. Isso dá mais folga quando chega uma foto ruim (luz, ângulo), exatamente o cenário do ônibus.

O **SFace** é da mesma família (restrições sobre a esfera), mas o treino dele foi pensado para não "decorar" fotos ruins do dataset. A literatura o descreve como mais estável em imagens degradadas. Daí o interesse por ele.

> 📌 **Na banca:** "ArcFace usa uma perda com margem angular aditiva, que força embeddings de pessoas diferentes a ficarem separados por uma margem na hiperesfera. Isso produz representações mais discriminativas que a triplet loss do FaceNet ou a classificação softmax dos modelos de 2014."

---

## 6. Os 10 modelos do benchmark

Agora a tabela do [resumo](estudo_reconhecimento_facial.md) deve fazer sentido. Agrupando por "geração":

| Geração | Modelos | Características |
|---|---|---|
| **2014–2015, pioneiros** | DeepFace (Facebook), DeepID, VGG-Face | Treinados por classificação. Grandes (VGG-Face ~580 MB) ou antigos. Hoje servem mais como **referência histórica**. |
| **2015–2016, aprendizado de métrica** | FaceNet (128 números), FaceNet512 (512 números), OpenFace | Triplet loss. OpenFace é uma versão leve e acadêmica do FaceNet. |
| **Prático/clássico** | Dlib | ResNet pequena, embedding de 128 números. Muito usado em projetos amadores (lib `face_recognition`). |
| **Moderno, margem angular** | **ArcFace**, **SFace**, GhostFaceNet | Estado da arte. SFace e GhostFaceNet foram projetados para ser **leves**, o que importa para o Pi. |

**Por que testar justamente esses 10?** Porque a biblioteca **DeepFace** (não confundir com o *modelo* DeepFace do Facebook) já empacota os 10 atrás da mesma função. Assim todos passam pelo **mesmo detector, alinhamento e dataset**, o que é a condição para uma **comparação justa**. Esse é um argumento metodológico bom para a monografia.

**Por que os números de "Acurácia (LFW)" da literatura (~99%) são tão maiores que os do seu benchmark (~50–93%)?** Os papers usam um **protocolo oficial** do LFW (pares fixos), com o **melhor detector e alinhamento** e um **limiar ajustado** para aquele teste. Você usou pares próprios, o detector mais fraco e o limiar padrão. Não é erro; são condições diferentes, e vale dizer isso explicitamente no texto.

---

## 7. Métricas: acurácia, precisão, recall e F1

### 7.1 Os quatro resultados possíveis

No benchmark, cada **par de fotos** tem a resposta verdadeira (mesma pessoa ou não) e o palpite do modelo. Cruzando os dois:

|  | Modelo diz **"mesma pessoa"** | Modelo diz **"pessoas diferentes"** |
|---|---|---|
| **É a mesma pessoa** | **VP**, verdadeiro positivo ✅ | **FN**, falso negativo ❌ (não reconheceu) |
| **São pessoas diferentes** | **FP**, falso positivo ❌ (confundiu) | **VN**, verdadeiro negativo ✅ |

Essa tabela se chama **matriz de confusão**. No código, são as variáveis `vp`, `fn`, `fp`, `vn` em `avaliar_modelo`.

**Traduzindo para o ônibus:**

- **FP (falso positivo):** o sistema marca **a Ana como presente quando quem entrou foi o João**. É grave: dá um registro falso de segurança (a Ana pode nem estar no ônibus).
- **FN (falso negativo):** a Ana entra e o sistema **não a reconhece**. É chato, mas recuperável: gera um alerta (RF-04), o monitor confere, ou o sistema tenta de novo no quadro seguinte do vídeo.

Ou seja, **os dois erros não pesam igual**. Em controle de presença de crianças, FP costuma ser pior que FN.

### 7.2 As métricas

| Métrica | Fórmula | Pergunta que responde |
|---|---|---|
| **Acurácia** | (VP + VN) / total | "De todos os pares, quantos acertei?" |
| **Precisão** | VP / (VP + FP) | "Quando eu disse 'mesma pessoa', quantas vezes estava certo?" (mede **confusões**) |
| **Recall** (sensibilidade) | VP / (VP + FN) | "Dos pares que eram mesma pessoa, quantos eu reconheci?" (mede **esquecimentos**) |
| **F1** | 2 × P × R / (P + R) | Média que equilibra precisão e recall; cai muito se uma das duas for baixa |

### 7.3 Exemplo com os números reais do seu benchmark

O benchmark tem **384 pares: 192 positivos** (mesma pessoa) **e 192 negativos**.

**SFace:** precisão 100%, recall 63,02%.

- Recall = 63,02% de 192 positivos → **VP = 121**, **FN = 71** (71 pares da mesma pessoa não reconhecidos)
- Precisão = 100% → **FP = 0** (nunca confundiu duas pessoas) → **VN = 192**
- Acurácia = (121 + 192) / 384 = **81,5%** ✔ (bate com a tabela)

**ArcFace:** precisão 99,40%, recall 85,94%.

- VP = 165, FN = 27, **FP = 1**, VN = 191
- Acurácia = (165 + 191) / 384 = **92,7%** ✔

**Leitura:** o SFace é "medroso". Nunca confunde ninguém, mas deixa de reconhecer 1 em cada 3 pares da mesma pessoa. O ArcFace reconhece bem mais e errou uma única confusão.

### 7.4 O limiar controla a troca entre precisão e recall

Lembra do limiar (seção 4.2)? Ele é o "botão" que troca uma métrica pela outra:

```
limiar mais exigente  ──▶  precisão ↑  recall ↓   (confunde menos, esquece mais)
limiar mais tolerante ──▶  precisão ↓  recall ↑   (esquece menos, confunde mais)
```

Precisão de 100% com recall baixo em vários modelos (SFace, GhostFaceNet, Facenet, OpenFace) é um sinal clássico de que **o limiar padrão está exigente demais para este cenário**. Ou seja, parte do resultado ruim pode ser só configuração, não o modelo. Uma análise mais completa varreria vários limiares e desenharia a **curva ROC**, que mostra todos os pares (taxa de acerto × taxa de confusão) possíveis. Essa curva é uma boa sugestão de próximo passo.

### 7.5 Nomes que aparecem na literatura de biometria

Artigos de biometria às vezes usam outros nomes para as mesmas ideias:

- **FAR** (*False Acceptance Rate*), ou FMR: taxa de falsa aceitação = FP / (FP + VN)
- **FRR** (*False Rejection Rate*), ou FNMR: taxa de falsa rejeição = FN / (FN + VP) = 1 − recall
- **EER** (*Equal Error Rate*): o ponto em que FAR = FRR; um número único para comparar sistemas

> 📌 **Na banca:** "Precisão mede confusões entre alunos; recall mede alunos não reconhecidos. No nosso contexto, falso positivo é mais grave que falso negativo, porque gera um registro falso de presença. Os modelos com precisão 100% e recall baixo indicam um limiar conservador, que pode ser recalibrado."

---

## 8. Lendo o benchmark do seu TCC

Com as seções anteriores, dá para ler o [relatório do benchmark](benchmark_reconhecimento_facial.md) com outros olhos.

### 8.1 O que o experimento fez, passo a passo

1. **Dataset:** LFW (*Labeled Faces in the Wild*), com fotos de pessoas públicas (adultos) tiradas "na natureza", com luz e ângulo variados. Foram usadas 96 pessoas com 15 ou mais fotos cada (`preparar_dataset.py`).
2. **Pares:** para cada pessoa, até 2 pares de fotos dela mesma (positivos), mais o mesmo número de pares sorteados entre pessoas diferentes (negativos). Total: 384.
3. **Para cada um dos 10 modelos:** chamar `DeepFace.verify` em cada par, que internamente **detecta → alinha → gera os 2 embeddings → mede a distância → compara com o limiar**.
4. **Contar** VP/FP/FN/VN, calcular as métricas e medir o tempo.
5. **Cada modelo roda em um processo separado** (seção 8.2).

### 8.2 O achado metodológico: isolamento de processos

Na primeira rodada, o SFace pareceu o mais lento (4,2 s por par), contradizendo a literatura. A causa: a biblioteca não descarrega modelos da memória, então quando chegava a vez do SFace, seis outros modelos estavam carregados ao mesmo tempo, disputando CPU e RAM. Rodando cada modelo **sozinho**, o SFace caiu para **0,089 s por par**, o mais rápido de todos.

Lição geral (boa para a monografia): **medir tempo exige isolar o que está sendo medido**. Senão você mede o ambiente, não o modelo.

### 8.3 Por que alguns modelos tiveram recall tão baixo

OpenFace (1,6% de recall) e DeepID (4,2%) praticamente nunca disseram "mesma pessoa". Três suspeitos, todos ligados a seções anteriores:

1. **Detector fraco (Haar):** em fotos de lado ou mal iluminadas, o Haar não acha o rosto. Como o script usa `enforce_detection=False`, o modelo recebe a **imagem inteira** em vez do rosto recortado, e o embedding sai ruim (seção 3.2).
2. **Limiar padrão inadequado** para estas imagens (seção 7.4).
3. **Modelos antigos de verdade** (DeepID, OpenFace), menos robustos.

Esse teste já foi feito com o **RetinaFace** (seção 7 do relatório), e a resposta foi "em parte". Com um detector melhor, o recall do ArcFace subiu de 86% para 94%, o do VGG-Face de 79% para 94% e o do Facenet de 53% para 65%. Mas o DeepID e o OpenFace continuaram perto de zero, e o SFace e o GhostFaceNet não mudaram. Ou seja: o suspeito 1 explicava parte do problema; para o SFace, o suspeito 2 (limiar) ficou mais forte, e para DeepID e OpenFace, o 3 (modelos antigos). Falta testar o **YuNet**.

### 8.4 A escolha preliminar: ArcFace + SFace

O cronograma pede para "escolher os 2 melhores de 10". O critério não é só acurácia, mas **acurácia × tempo × tamanho**, porque o modelo precisa caber e rodar no ônibus:

| | ArcFace | SFace |
|---|---|---|
| Papel | "O mais preciso" | "O mais leve" |
| Acurácia | 92,7% (melhor) | 81,5% (com precisão 100%) |
| Tempo/par (no PC) | 0,74 s | **0,089 s** (melhor) |
| Tamanho | 130 MB (existe versão MobileFaceNet de ~4 MB) | **5 MB** |

### 8.5 Limitações para declarar honestamente na monografia

- **Adultos famosos, não crianças em ônibus.** Rostos infantis mudam com o crescimento, e as condições do LFW não são as do ônibus.
- **384 pares** é uma amostra pequena; diferenças de 1–2 pontos percentuais podem ser ruído.
- **Tempo medido num PC**, não no Raspberry Pi/Hailo; o número absoluto vai mudar (a ordem relativa tende a se manter).
- **Verificação 1:1**, enquanto o sistema real faz identificação 1:N (seção 4.3).
- **Dois detectores (Haar e RetinaFace) e um limiar só**, o padrão do DeepFace.

### 8.6 Mapa do código para os conceitos

Para quem tem Python básico, aqui está [benchmark_reconhecimento_facial.py](../pesquisa/benchmark_reconhecimento_facial.py) traduzido:

| Trecho do código | O que faz | Conceito |
|---|---|---|
| `MODELOS = [...]` | Lista dos 10 modelos a testar | Seção 6 |
| `DETECTOR_PADRAO = "opencv"` | Escolhe o detector Haar Cascade | Seção 3 |
| `montar_pares(...)` | Lê as pastas (uma por pessoa) e monta pares positivos e negativos | Seção 8.1 |
| `DeepFace.verify(img1, img2, model_name=..., detector_backend=...)` | Detecta, alinha, gera embeddings, mede a distância e aplica o limiar. Devolve `verified` = True/False | Seções 3 e 4 |
| `enforce_detection=False` | Se não achar rosto, segue com a imagem inteira em vez de dar erro | Seção 8.3 |
| `if par.mesma_pessoa and previsto_mesma_pessoa: vp += 1 ...` | Preenche a matriz de confusão | Seção 7.1 |
| `acuracia = (vp + vn) / total` etc. | Calcula as métricas | Seção 7.2 |
| `time.perf_counter()` antes e depois | Mede o tempo de cada par | Seção 8.2 |
| `multiprocessing` / `spawn` | Roda cada modelo num processo isolado | Seção 8.2 |

---

## 9. Hardware embarcado e edge computing

### 9.1 Computador × microcontrolador

| | **Raspberry Pi** (ex.: Pi 5) | **ESP32** |
|---|---|---|
| O que é | **Computador** completo do tamanho de um cartão | **Microcontrolador**: um chip simples que roda um único programa |
| Sistema operacional | Linux (roda Python, OpenCV, etc. normalmente) | Nenhum completo (programa em C/C++, ou MicroPython limitado) |
| Memória RAM | **GBs** (2 a 16 GB) | **KBs** (~520 KB, ou alguns MB com memória extra) |
| Consumo/custo | Maior | Muito baixo |
| Rodar ArcFace/SFace | Sim | **Não** na forma padrão: a RAM é centenas a milhares de vezes menor que o modelo |

**Conclusão que já está nas suas anotações:** um modelo de 5 MB (SFace), o menor do topo do ranking, não cabe nos ~0,5 MB de RAM de um ESP32. Isso é um argumento direto para a escolha do **Raspberry Pi** na Atividade 1.3. O ESP32 só roda redes drasticamente reduzidas (ex.: o projeto ESP-WHO da Espressif), com qualidade bem menor.

### 9.2 Acelerador de IA: o Hailo AI HAT

A CPU do Pi consegue rodar os modelos, mas devagar. O **AI HAT** é uma placa que encaixa no Pi e traz uma **NPU** (*Neural Processing Unit*), um chip especializado só em fazer as contas de redes neurais, muito mais rápido e gastando menos energia que a CPU. Modelos citados: Hailo-8L, Hailo-8, Hailo-10H.

A pegadinha: a NPU **não roda qualquer arquivo de modelo**. É preciso **converter** o modelo para o formato dela (HEF, no caso do Hailo), o que motiva a tarefa de 30/11 do cronograma ("emular o ambiente do Hailo no computador e ver se precisa trocar a linguagem").

### 9.3 Formatos e otimização de modelos

- **TensorFlow / Keras:** a biblioteca em que muitos modelos foram treinados (ver [anotações](revisao_bibliografica.md), seção 2).
- **TensorFlow Lite (TFLite):** versão "enxuta" para celular e embarcados. Está na stack do projeto.
- **ONNX:** um formato "neutro" de modelo, que muitas ferramentas leem; a ponte comum entre frameworks. O SFace e o YuNet do OpenCV já vêm em ONNX.
- **HEF:** formato compilado específico do Hailo.
- **Quantização:** guardar os pesos com menos precisão, por exemplo números de 8 bits (int8) em vez de 32 bits (float32). O modelo fica **~4× menor e mais rápido**, com uma perda pequena de acurácia. NPUs como a do Hailo geralmente **exigem** modelos quantizados. Por isso a acurácia medida no PC pode cair um pouco no dispositivo: é algo a medir no TCC 2.

### 9.4 Edge computing: por que processar no ônibus e não na nuvem

**Edge (borda)** significa processar **no próprio dispositivo**, perto de onde o dado nasce, em vez de mandar o vídeo para um servidor na nuvem. No projeto isso é requisito (RNF-13) por três motivos:

1. **Conectividade:** a zona rural tem 4G instável; mandar vídeo não seria viável.
2. **Latência:** a decisão precisa sair em segundos, na porta do ônibus.
3. **Privacidade:** se o vídeo nunca sai do ônibus, o risco de vazamento cai muito (seção 12).

> 📌 **Na banca:** "O ESP32 não tem memória para nenhum dos modelos avaliados, então a arquitetura aponta para Raspberry Pi com um acelerador Hailo. Isso exige converter e quantizar os modelos, o que pode alterar a acurácia e será validado no TCC 2. O processamento é na borda por conectividade, latência e privacidade."

---

## 10. Comunicação: MQTT no contexto do projeto

Você já conhece o modelo publish/subscribe. O que vale ligar ao projeto:

- **O que trafega é pequeno:** só o **evento** (`{aluno_id, onibus, rota, horario, tipo: "embarque"}`), nunca imagem. Cabe bem em MQTT, que foi feito para mensagens pequenas em redes ruins.
- **QoS (*Quality of Service*):** o MQTT tem 3 níveis de garantia de entrega: 0 = "no máximo uma vez", 1 = "pelo menos uma vez", 2 = "exatamente uma vez". O **RF-08** ("nenhum evento perdido ou duplicado") conversa diretamente com isso. Uma abordagem comum é QoS 1 com um **identificador único por evento**, para o servidor descartar duplicatas.
- **Fila offline (RF-07):** sem sinal, os eventos ficam num banco local no Pi e são publicados quando a conexão volta.

---

## 11. Reconhecimento de voz

Ainda não há trabalho prático sobre voz no repositório, mas ela está no título do TCC. O essencial:

- **Não confundir:** *reconhecimento de fala* (*speech recognition*) = **o que** foi dito (transcrição). *Reconhecimento de locutor* (*speaker recognition*) = **quem** falou. **O projeto precisa do segundo.**
- **A ideia é a mesma do rosto:** o áudio vira uma imagem do som, o **espectrograma** (ou coeficientes **MFCC**). Uma rede neural transforma isso em um **embedding de voz** (nomes comuns: *x-vector*, *ECAPA-TDNN*), e compara-se com os cadastrados por distância e limiar. Tudo da seção 4 e da seção 7 se aplica.
- **Desafio específico do ônibus:** ruído (motor, estrada, outras crianças falando) e voz infantil que muda com a idade.
- **Fusão multimodal:** combinar rosto e voz. Por exemplo, voz como **confirmação** quando o rosto der baixa confiança (é isso que o RF-02 sugere, "mecanismo complementar"). Combinar duas evidências independentes reduz erros.

---

## 12. LGPD e dados biométricos

Pontos que você precisa saber para a Atividade 1.4 e para a banca:

- **Biometria é dado pessoal sensível** (LGPD, art. 5º, II), com regras mais rígidas de tratamento (art. 11).
- **Crianças e adolescentes** (art. 14): o tratamento deve ser no **melhor interesse** deles e, para crianças, exige **consentimento específico e em destaque de pelo menos um dos pais ou responsável legal**.
- **Embedding também é dado biométrico.** Guardar só o vetor em vez da foto é uma ótima prática de **minimização** (RF-05, RNF-07), mas **não torna o dado anônimo**: ele continua identificando a pessoa. Por isso o RNF-10 pede criptografia também dos embeddings.
- **Por que o benchmark usa LFW, e não fotos de alunos:** fase de prototipagem, sem base legal ainda formalizada (restrição RC-01). Datasets públicos de adultos são o caminho correto.
- **Viés:** modelos de rosto treinados majoritariamente com adultos podem funcionar pior com **crianças** e com alguns grupos demográficos. Vale citar como risco ético e técnico.

---

## 13. Glossário

| Termo | Significado curto |
|---|---|
| **Acurácia** | Fração de acertos sobre o total |
| **Alinhamento** | Girar e recortar o rosto para os olhos ficarem em posição padrão |
| **Backbone** | A arquitetura de rede "base" de um modelo (ResNet, MobileNet…) |
| **Bounding box** | Retângulo que delimita o rosto na imagem |
| **CNN** | Rede neural convolucional, o tipo de rede usado para imagens |
| **Detecção** | Achar *onde* há um rosto |
| **Distância cosseno** | Medida de diferença entre dois embeddings (0 = iguais) |
| **Edge / borda** | Processar no próprio dispositivo, não na nuvem |
| **Embedding / template** | Vetor de números que representa um rosto (ou voz) |
| **Enrollment / cadastro** | Registrar o embedding de referência de uma pessoa |
| **F1** | Média harmônica de precisão e recall |
| **FAR / FRR** | Taxas de falsa aceitação e falsa rejeição (nomes biométricos para FP e FN) |
| **Identificação (1:N)** | Descobrir quem é entre N cadastrados |
| **Inferência** | Usar um modelo já treinado |
| **Landmarks** | Pontos-chave do rosto (olhos, nariz, boca) |
| **LFW** | Dataset público de referência para reconhecimento facial |
| **Limiar / threshold** | Valor de distância que separa "mesma pessoa" de "diferente" |
| **Loss / função de perda** | Medida de erro usada para treinar o modelo |
| **Margem angular** | Técnica do ArcFace que força separação entre pessoas na esfera |
| **NPU** | Chip especializado em redes neurais (ex.: Hailo) |
| **ONNX / TFLite / HEF** | Formatos de arquivo de modelos |
| **Pré-treinado** | Modelo já treinado por terceiros, pronto para uso |
| **Precisão** | Dos "sim" que o modelo disse, quantos estavam certos |
| **Quantização** | Reduzir a precisão numérica dos pesos para o modelo ficar menor e mais rápido |
| **Recall** | Dos "sim" verdadeiros, quantos o modelo achou |
| **Reconhecimento** | Descobrir *de quem* é o rosto |
| **Verificação (1:1)** | Decidir se duas amostras são da mesma pessoa |

---

## 14. Autoavaliação

Tente responder antes de abrir a resposta. As três primeiras são as do diagnóstico.

<details>
<summary><b>1.</b> No pipeline, qual a diferença entre o que YuNet/RetinaFace e ArcFace/SFace fazem?</summary>

YuNet/RetinaFace são **detectores**: dizem *onde* está o rosto (caixa + landmarks). ArcFace/SFace são **reconhecedores**: transformam o rosto recortado em um embedding para descobrir *de quem* ele é. São etapas em sequência, não alternativas.
</details>

<details>
<summary><b>2.</b> O que o ArcFace devolve quando recebe a foto de um rosto?</summary>

Um **vetor de 512 números** (embedding). Fotos da mesma pessoa geram vetores próximos. O nome sai só depois, comparando esse vetor com os cadastrados.
</details>

<details>
<summary><b>3.</b> SFace teve precisão 100% e recall 63%. O que isso significa?</summary>

Ele **nunca confundiu** duas pessoas diferentes (zero falsos positivos), mas **não reconheceu ~37%** dos pares que eram da mesma pessoa (71 falsos negativos). Indica um limiar conservador.
</details>

<details>
<summary><b>4.</b> Por que o modelo funciona com alunos que ele nunca viu no treino?</summary>

Porque ele não decorou pessoas: aprendeu a gerar embeddings em que "rostos diferentes ficam longe". Basta cadastrar o embedding de cada aluno e comparar por distância.
</details>

<details>
<summary><b>5.</b> O benchmark mede verificação ou identificação? E o sistema real?</summary>

O benchmark mede **verificação 1:1** (pares). O sistema real faz **identificação 1:N** (um rosto contra ~20 alunos). É uma limitação a declarar.
</details>

<details>
<summary><b>6.</b> No ônibus, o que é pior: falso positivo ou falso negativo? Por quê?</summary>

Em geral o **falso positivo**: registra presença de quem não está no ônibus (falsa segurança). O falso negativo gera um alerta e pode ser conferido ou repetido no próximo quadro do vídeo.
</details>

<details>
<summary><b>7.</b> Se eu tornar o limiar mais tolerante, o que acontece com precisão e recall?</summary>

O recall sobe (reconhece mais) e a precisão tende a cair (confunde mais).
</details>

<details>
<summary><b>8.</b> Cite duas causas possíveis do recall baixíssimo de OpenFace e DeepID no benchmark.</summary>

Detector Haar fraco (com `enforce_detection=False`, o modelo recebe a imagem inteira quando o rosto não é achado), limiar padrão inadequado e o fato de serem modelos antigos.
</details>

<details>
<summary><b>9.</b> Por que o ESP32 não serve para rodar SFace?</summary>

O ESP32 é um microcontrolador com ~520 KB de RAM. O SFace, o menor modelo do topo do ranking, tem ~5 MB. Além disso, o ESP32 não tem sistema operacional para rodar OpenCV ou Python completo.
</details>

<details>
<summary><b>10.</b> O que é quantização e por que ela importa para o Hailo?</summary>

É guardar os pesos com menos bits (ex.: int8 em vez de float32): o modelo fica ~4× menor e mais rápido, com pequena perda de acurácia. NPUs como a Hailo geralmente exigem modelos quantizados, então a acurácia precisa ser medida de novo no dispositivo.
</details>

<details>
<summary><b>11.</b> Guardar só o embedding, e não a foto, torna o dado anônimo perante a LGPD?</summary>

**Não.** O embedding continua sendo dado biométrico (sensível) e identifica a pessoa. É uma boa prática de minimização, mas exige consentimento dos responsáveis e proteção (criptografia).
</details>

<details>
<summary><b>12.</b> Por que o SFace parecia o mais lento na primeira rodada?</summary>

Porque todos os modelos rodavam no mesmo processo, e a biblioteca não descarrega modelos, então seis modelos estavam na memória disputando CPU. Isolando cada modelo em um processo, o SFace caiu para 0,089 s por par.
</details>

Onde reler se errar: 1 → seção 3 · 2, 4, 5 → seção 4 · 3, 6, 7 → seção 7 · 8, 12 → seção 8 · 9, 10 → seção 9 · 11 → seção 12. Se acertar 10 de 12 ou mais, você está pronta para acompanhar o trabalho.

---

## 15. O que estudar depois

Em ordem de prioridade para o cronograma:

1. **Até 31/10 (escolher os 2 modelos):** o `retinaface` já foi testado (seção 8.3); falta rodar o benchmark com `--detector_backend yunet --cache_deteccao` e comparar o recall. Se possível, testar alguns limiares (seção 7.4) — agora é o principal suspeito do recall baixo do SFace.
2. **Atividade 1.3 (arquitetura):** ler sobre o Raspberry Pi 5 + AI HAT (Hailo) e o fluxo de conversão de modelo (ONNX → HEF, quantização).
3. **Atividade 1.4 (impactos):** ler os arts. 5º, 11 e 14 da LGPD e buscar material sobre viés de reconhecimento facial em crianças.
4. **Para a revisão bibliográfica**, os artigos originais a citar:
   - Viola & Jones (2001), Haar Cascade
   - Taigman et al. (2014), DeepFace
   - Schroff et al. (2015), FaceNet
   - Deng et al. (2019), ArcFace e RetinaFace
   - Zhong et al. (2021), SFace
   - Huang et al. (2007), dataset LFW

   Ao ler, foque na *introdução* e na *seção de resultados*. Não precisa entender as fórmulas da parte de métodos.
5. **Opcional, para ganhar intuição de deep learning:** a série em vídeo "Neural Networks" do canal 3Blue1Brown (YouTube, com legenda em português). São ~1 h no total e cobrem as seções 2 e 5 visualmente.
