# Guia de leitura: reconhecimento facial com aprendizado profundo em sistemas embarcados (Lv, Su e Wang, 2021)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (Elsevier), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** LV, X.; SU, M.; WANG, Z. Application of face recognition method under deep learning algorithm in embedded systems. *Microprocessors and Microsystems*, 2021, artigo 104034. DOI: [10.1016/j.micpro.2021.104034](https://doi.org/10.1016/j.micpro.2021.104034).
> **PDF local:** `Downloads/Referencias/lv_2021_reconhecimento_facial_sistemas_embarcados.pdf` (há uma cópia idêntica com sufixo `_duplicado`, que pode ser apagada).
>
> **Atenção:** o PDF da pasta é a versão *pre-proof* (antes da revisão final). Confira os números na versão publicada antes de citá-los (item E4 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).

---

## Em uma frase

Os autores montam um sistema embarcado de reconhecimento facial combinando um detector MTCNN otimizado e uma CNN leve de reconhecimento, e mostram que dá para manter boa acurácia reduzindo bastante o custo de cálculo.

## O problema

Redes profundas de reconhecimento facial são precisas, mas pesadas para processadores embarcados. A questão é como adaptar a detecção e o reconhecimento para caber em hardware limitado, sem perder muito em acurácia.

## O que eles propõem

1. **OMTCNN (detecção):** uma versão otimizada da MTCNN, uma rede em cascata de três estágios muito usada para detectar e alinhar rostos. A otimização mexe no pré-processamento (transformações simuladas e recortes do rosto) para melhorar o treino.
2. **LCNN (reconhecimento):** uma CNN leve, com menos camadas e parâmetros, para gerar o descritor do rosto com menor custo.
3. **Sistema embarcado:** junta os dois em uma plataforma embarcada de vários núcleos, distribuindo as etapas entre os núcleos.
4. Os testes de tempo são feitos em mais de uma plataforma embarcada (o [documento de lacunas](../lacunas_revisao_bibliografica.md) registra Raspberry Pi, Intel NCS e Jetson TX2), e não só no PC.

## Resultados principais

- O OMTCNN atingiu cerca de 95,8% de acurácia no treino, melhor que a MTCNN sem a otimização.
- A LCNN teve cerca de 98,1% de acerto na LFW.
- A redução de complexidade deixou o processamento até cerca de 6,4 vezes mais rápido.

## Limitações

- A acurácia de treino do detector não diz muito sobre o desempenho em dados novos.
- Os 98,1% na LFW ficam abaixo dos modelos de referência (ArcFace passa de 99,8%), o que é o preço da leveza.
- Versão *pre-proof*: números e figuras podem ter mudado na publicação final.

## Ligação com o TCC

- Mostra a abordagem que o projeto também segue: escolher detector e reconhecedor pensando no hardware, e medir o tempo **no dispositivo**, não no PC (item M4 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).
- Reforça o achado do benchmark de que a detecção pesa tanto quanto o reconhecimento: o artigo dedica metade do trabalho só ao detector.
- Útil na comparação Raspberry Pi × aceleradores (Hailo, no caso do projeto), já que testa mais de uma plataforma.

## Perguntas para conferir a leitura

1. Por que a MTCNN é chamada de rede "em cascata", e qual a vantagem disso para hardware limitado?
2. O ganho de 6,4 vezes em velocidade compensa a perda de acurácia em relação ao ArcFace no cenário do ônibus?
3. Em que hardware cada número de tempo foi medido?
