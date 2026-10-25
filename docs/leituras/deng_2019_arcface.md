# Guia de leitura: ArcFace (Deng, Guo, Xue e Zafeiriou, 2019)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE/CVF; versão aberta no arXiv), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** DENG, J.; GUO, J.; XUE, N.; ZAFEIRIOU, S. ArcFace: additive angular margin loss for deep face recognition. In: IEEE/CVF CVPR, 2019. *Proceedings* [...]. p. 4690–4699. DOI: [10.1109/CVPR.2019.00482](https://doi.org/10.1109/CVPR.2019.00482) · versão aberta: [arXiv 1801.07698](https://arxiv.org/abs/1801.07698).
> **PDF local:** `Downloads/Referencias/deng_2019_arcface.pdf` · **Chave no .bib:** `deng2019arcface`

---

## Em uma frase

A ArcFace é uma **função de perda** para treinar redes de reconhecimento facial: ela soma uma margem fixa ao **ângulo** entre o *embedding* de uma foto e o centro da sua classe, o que força fotos da mesma pessoa a ficarem bem agrupadas e pessoas diferentes bem separadas.

## Contexto: a evolução das perdas

- **Softmax simples:** separa as pessoas do treino, mas não deixa margem; os *embeddings* não ficam bons para comparar pessoas novas.
- **Center loss:** puxa cada *embedding* para o centro da sua classe (é a usada no FN8, de Deng *et al.*, 2023).
- **Triplet loss (FaceNet):** funciona, mas depende de escolher bons trios e o número de trios cresce muito.
- **SphereFace e CosFace:** passam a trabalhar com ângulos sobre uma hiperesfera e introduzem margens. A SphereFace multiplica o ângulo; a CosFace subtrai uma margem do cosseno.
- **ArcFace:** soma a margem **direto no ângulo**.

## Como a perda funciona, sem fórmulas

1. O *embedding* da foto e o vetor de pesos de cada pessoa do treino são normalizados para comprimento 1, ficando sobre uma esfera. A semelhança entre eles passa a ser só o ângulo.
2. Para a classe correta, o ângulo recebe um acréscimo fixo (a margem, tipicamente 0,5 radiano) antes de virar a "nota" da classe. Assim, para acertar, a rede precisa deixar o *embedding* bem mais perto do seu centro do que seria necessário sem a margem.
3. Um fator de escala (tipicamente 64) ajusta o tamanho das notas para o treino convergir.
4. Como a margem é somada ao ângulo, ela corresponde a uma distância fixa sobre a superfície da esfera (distância geodésica), daí a "interpretação geométrica clara" que os autores destacam.

## Outras contribuições do artigo

- Comparação cuidadosa com SphereFace, CosFace e combinações de margens.
- Limpeza de bases de treino públicas (as versões "MS1MV2" etc.), que viraram padrão na área.
- Avaliação em muitas bases: LFW, CFP-FP, AgeDB, CPLFW, CALFW, YTF, MegaFace, IJB-B, IJB-C, entre outras.

## Resultados principais

- Com uma ResNet de 100 camadas treinada na MS1MV2 (5,8 milhões de fotos), 99,83% na LFW e resultados de referência em MegaFace e IJB-B/C, à frente da SphereFace e da CosFace.
- A margem aditiva no ângulo foi a que deu os melhores resultados entre as variantes testadas.

## Limitações

- Bases de treino com rótulos errados e fotos ruins prejudicam o treino, porque a margem força demais todos os exemplos. É exatamente o ponto que a SFace (Zhong *et al.*, 2021) tenta resolver.
- O artigo avalia sobretudo acurácia; custo em hardware embarcado não é o foco.

## Ligação com o TCC

- **Ponto mais importante para a monografia:** "ArcFace" é a perda, não uma rede. O que o benchmark testou é a ResNet treinada com ArcFace da biblioteca DeepFace (item E1 do [documento de lacunas](../lacunas_revisao_bibliografica.md)). ELANet, MobileFaceNet, PocketNet e outros modelos leves também são treinados com ArcFace.
- Foi o melhor modelo do benchmark do projeto (96,61% com RetinaFace).
- Como a ArcFace organiza os rostos por ângulo, a comparação natural entre *embeddings* é a distância de cosseno; isso pesa na hora de calibrar o limiar.

## Perguntas para conferir a leitura

1. Qual a diferença entre somar a margem ao ângulo (ArcFace) e subtraí-la do cosseno (CosFace)?
2. Por que normalizar os vetores faz a semelhança depender só do ângulo?
3. Por que dizer "testamos o ArcFace" é impreciso, e como escrever isso corretamente na monografia?
