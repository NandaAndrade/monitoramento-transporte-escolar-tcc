# Guia de leitura: RetinaFace (Deng *et al.*, 2020)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE/CVF; versão aberta no arXiv), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** DENG, J.; GUO, J.; VERVERAS, E.; KOTSIA, I.; ZAFEIRIOU, S. RetinaFace: single-shot multi-level face localisation in the wild. In: IEEE/CVF CVPR, 2020. *Proceedings* [...]. p. 5203–5212. DOI: [10.1109/CVPR42600.2020.00525](https://doi.org/10.1109/CVPR42600.2020.00525) · versão aberta: [arXiv 1905.00641](https://arxiv.org/abs/1905.00641).
> **PDF local:** `Downloads/Referencias/deng_2020_retinaface.pdf` · **Chave no .bib:** `deng2020retinaface`

---

## Em uma frase

O RetinaFace é um detector de rostos que, numa única passada da rede, devolve a **caixa do rosto**, **cinco pontos de referência** (olhos, ponta do nariz, cantos da boca) e uma **malha 3D** do rosto; essa supervisão extra torna a detecção mais precisa, sobretudo em rostos difíceis.

## O problema

Detectores de rosto já eram bons em condições normais, mas erravam em rostos pequenos, de lado, parcialmente cobertos ou borrados. Além disso, o reconhecimento facial precisa do rosto **alinhado**, e isso exige pontos de referência confiáveis.

## A ideia central

1. **Uma rede, várias tarefas:** além de dizer onde há um rosto, a rede também prevê os cinco pontos e os vértices de uma malha 3D projetados na imagem. Aprender essas tarefas juntas ajuda a detecção.
2. **Mais anotação:** os autores anotaram à mão os cinco pontos em cerca de 84,6 mil rostos do treino e 18,5 mil da validação da base WIDER FACE, e geraram vértices 3D de forma semiautomática.
3. **Malha 3D auto-supervisionada:** um decodificador de malha reconstrói o rosto em 3D e o renderiza de volta em 2D; a diferença entre a imagem renderizada e a original serve de sinal de treino, sem precisar de anotação 3D completa.
4. **Detecção de estágio único em vários níveis:** usa uma pirâmide de características (como no detector de objetos RetinaNet) para achar rostos de tamanhos muito diferentes na mesma imagem.

## Resultados principais

- Na base WIDER FACE, o subconjunto "difícil" (rostos pequenos e complicados) chegou a cerca de 91,4% de precisão média, à frente dos detectores da época. O estudo de ablação mostra que cada tarefa extra (pontos e malha) melhora um pouco o resultado.
- Usar o RetinaFace para **alinhar** os rostos melhora o reconhecimento com ArcFace em bases como a IJB-C.
- Há uma versão leve (base MobileNet) que roda em tempo real em CPU para imagens VGA, com acurácia menor que a versão ResNet.

## Limitações

- A versão de maior acurácia (base ResNet-50 ou maior) é pesada para hardware embarcado.
- A malha 3D aumenta o custo de treino; na prática, a maioria das bibliotecas usa só caixa e cinco pontos.

## Ligação com o TCC

- Foi o detector que mais melhorou o benchmark do projeto: ArcFace de 92,97% para 96,61%, porque os rostos passaram a ser encontrados e alinhados com os cinco pontos.
- O custo apareceu claramente: cerca de 0,62 s por imagem na CPU do PC, deixando o ArcFace em 1,80 s por par, perto do limite de 2 s do RNF-02. No Raspberry Pi, isso só fecha com o acelerador Hailo ou com a versão MobileNet.
- O YuNet (Wu *et al.*, 2023), também nesta pasta, é o candidato leve a comparar com ele.

## Perguntas para conferir a leitura

1. Por que prever pontos de referência ajuda a própria detecção do rosto?
2. Para que o reconhecimento facial precisa dos cinco pontos?
3. Que versão do RetinaFace faria sentido testar no Raspberry Pi, e qual seria a perda esperada?
