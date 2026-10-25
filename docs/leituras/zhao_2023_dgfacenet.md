# Guia de leitura: DGFaceNet (Zhao, Zhang, Zhang e Li, 2023)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (Elsevier), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** ZHAO, F.; ZHANG, P.; ZHANG, R.; LI, M. DGFaceNet: lightweight and efficient face recognition. *Engineering Applications of Artificial Intelligence*, v. 124, artigo 106513, 2023. Confira o DOI na página do artigo.
> **PDF local:** `Downloads/Referencias/zhao_2023_dgfacenet.pdf`

---

## Em uma frase

O DGFaceNet é uma rede leve de reconhecimento facial que gera parte das suas características com **operações baratas** ("características fantasma") e é treinada com uma nova perda pensada para redes pequenas; o resultado roda várias vezes mais rápido que as redes leves conhecidas em dispositivos embarcados.

## O problema

Redes leves precisam economizar cálculo sem perder muita acurácia. Além disso, as perdas populares (como ArcFace e CosFace) foram pensadas para redes grandes: em redes pequenas, com vetores de saída de poucas dimensões, o treino pode não convergir ou ficar instável.

## As duas ideias principais

1. **Dynamic Ghost Bottleneck:**
   - A ideia "fantasma" (da GhostNet) parte da observação de que muitos mapas de características de uma CNN são parecidos entre si. Em vez de calcular todos com convoluções caras, calcula-se uma parte e gera-se o resto com operações lineares baratas.
   - Os autores mostram que a rede **tolera mais características baratas no início** do que no fim. Por isso, ajustam dinamicamente a proporção de características baratas ao longo da profundidade da rede. O DGFaceNet é a pilha desses blocos.
2. **CML-softmax (nova função de perda):**
   - Troca a função cosseno, usada nas perdas de margem como nota da classe correta, por uma **função quadrática**, que se comporta melhor quando o vetor de saída tem poucas dimensões.
   - Acrescenta duas funções de margem: uma para o **desbalanceamento de classes** (pessoas com muito mais fotos que outras na base de treino) e outra para a **saturação precoce** da softmax (quando o treino para de aprender cedo demais).

## Resultados principais

- Resultados competitivos em várias bases de validação (LFW e variantes como CFP-FP, AgeDB, CALFW, CPLFW) e em testes de grande escala (IJB-B/C, MegaFace).
- **Testes de velocidade em dispositivos embarcados:** o tempo real de inferência foi cerca de 11 vezes menor que o da ResNet-50, 8,6 vezes menor que o da EfficientNet e cerca de 2,8 vezes menor que o da MobileNetV2 e do MobileFaceNet.

## Limitações

- O modelo não está disponível em bibliotecas prontas como a DeepFace; usá-lo exigiria treinar ou converter a rede.
- Os ganhos de velocidade dependem do hardware usado no teste; no Hailo, operações diferentes podem ter custos diferentes.

## Ligação com o TCC

- É do mesmo grupo do ELANet (Zhang *et al.*, 2022, traduzido nesta pasta); juntos, mostram a linha de pesquisa de redes leves com perdas de margem.
- Diferente do ELANet, **mede tempo em dispositivo embarcado**, o que é o dado que mais interessa ao projeto.
- Item E2 do [documento de lacunas](../lacunas_revisao_bibliografica.md): o DGFaceNet compara com um "GhostFaceNet" do mesmo grupo, que não é o GhostFaceNet testado no benchmark (o da biblioteca DeepFace é de Alansari *et al.*, 2023). Não use os números do GhostFaceNet deste artigo como referência para o modelo do benchmark.

## Perguntas para conferir a leitura

1. O que são "características fantasma" e por que elas economizam cálculo?
2. Por que a rede tolera mais características baratas no início do que no fim?
3. Que dois problemas de treino a CML-softmax tenta resolver?
