# Guia de leitura: YuNet (Wu, Peng e Yu, 2023)

> **Guia de estudo em português**, não é tradução. O PDF não traz licença aberta explícita, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** WU, W.; PENG, H.; YU, S. YuNet: a tiny millisecond-level face detector. *Machine Intelligence Research*, v. 20, n. 5, p. 656–665, 2023. DOI: [10.1007/s11633-023-1423-y](https://doi.org/10.1007/s11633-023-1423-y).
> **PDF local:** `Downloads/Referencias/wu_2023_yunet.pdf` · **Chave no .bib:** `wu2023yunet`

---

## Em uma frase

O YuNet é um detector de rostos minúsculo (cerca de 76 mil parâmetros), feito para dispositivos de borda, que roda em **milissegundos** na CPU e mantém acurácia competitiva.

## O problema

Os detectores mais precisos, como o RetinaFace, são pesados demais para celulares e placas embarcadas. Os autores querem o melhor equilíbrio possível entre acurácia e velocidade, com um modelo pequeno o bastante para caber em qualquer dispositivo.

## A ideia central

1. **Análise dos detectores existentes:** os autores estudam onde estão os parâmetros e as operações dos detectores recentes e tiram regras práticas para encolher modelos (por exemplo, reduzir o número de canais nas camadas de maior resolução e simplificar a fusão de escalas).
2. **Rede de base minúscula:** usa convoluções separáveis em profundidade e poucos canais.
3. **Pescoço piramidal simplificado:** funde características de algumas escalas com pouquíssimo custo, para detectar rostos grandes e pequenos.
4. **Sem âncoras (*anchor-free*):** em vez de testar caixas pré-definidas de vários tamanhos, cada posição da imagem prevê diretamente se há um rosto e onde; isso reduz cálculo e simplifica o pós-processamento.
5. Além da caixa, prevê os cinco pontos de referência, o que permite alinhar o rosto para o reconhecimento.

## Resultados principais

- 75.856 parâmetros, menos de um quinto do tamanho dos detectores leves que existiam.
- 81,1% de precisão média no subconjunto "difícil" da WIDER FACE (validação, escala única). É menos que o RetinaFace grande, mas muito à frente do Haar e de outros detectores leves no mesmo custo.
- Tempo de poucos milissegundos por imagem em CPU de computador, daí o "milissegundo" do título.
- Está integrado ao OpenCV (classe `FaceDetectorYN`), o que facilita o uso em Python no Raspberry Pi.

## Limitações

- Perde acurácia nos rostos muito pequenos e muito difíceis, justamente onde o RetinaFace é forte.
- Os tempos relatados são em CPU de computador; no Raspberry Pi o tempo será maior e precisa ser medido.

## Ligação com o TCC

- É o **próximo detector a testar no benchmark**, como já registrado no relatório de 11/10 e na Visão Geral.
- Pergunta central: o YuNet chega perto do ganho que o RetinaFace deu ao ArcFace (de 92,97% para 96,61%), mas custando milissegundos em vez de 0,6 s por imagem? Se sim, ele resolve o aperto no limite de 2 s do RNF-02.
- Na porta do ônibus, os rostos estarão perto da câmera e relativamente grandes; o ponto fraco do YuNet (rostos minúsculos) pesa pouco nesse cenário.

## Perguntas para conferir a leitura

1. O que significa um detector "sem âncoras" e por que isso economiza cálculo?
2. Por que os cinco pontos de referência continuam importantes mesmo num detector minúsculo?
3. Em que tipo de rosto o YuNet perde mais para o RetinaFace, e isso é relevante na porta do ônibus?
