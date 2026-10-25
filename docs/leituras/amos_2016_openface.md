# Guia de leitura: OpenFace, biblioteca aberta de reconhecimento facial (Amos *et al.*, 2016)

> **Guia de estudo em português**, não é tradução. O relatório técnico não traz licença aberta para o texto (a licença Apache 2.0 é do código), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** AMOS, B.; LUDWICZUK, B.; SATYANARAYANAN, M. OpenFace: A general-purpose face recognition library with mobile applications. Relatório técnico CMU-CS-16-118. Pittsburgh: Carnegie Mellon University, jun. 2016.
> **PDF local:** `docs/Referencias/amos_2016_openface.pdf` · **Chave no .bib:** `amos2016openface`
>
> **Atenção ao nome:** existe outro projeto chamado OpenFace, de análise de expressões faciais (Baltrušaitis *et al.*). O modelo da biblioteca DeepFace usada no benchmark é este, da Carnegie Mellon.

---

## Em uma frase

O OpenFace é uma biblioteca de código aberto que reproduz a ideia do FaceNet com uma rede menor, treinada só com bases públicas, para diminuir a distância entre os sistemas abertos e os das grandes empresas e permitir o uso em cenários móveis e de IoT.

## O problema

Os melhores sistemas da época (DeepFace, FaceNet) usavam bases privadas de milhões de fotos e não eram públicos. As bibliotecas abertas, como as do OpenCV (Eigenfaces, Fisherfaces, LBPH), tinham acurácia muito menor. Os autores querem uma biblioteca aberta, precisa e rápida o bastante para dispositivos móveis, câmeras e IoT.

## Como a biblioteca funciona

1. **Detecção:** acha os rostos na imagem.
2. **Alinhamento:** localiza 68 pontos do rosto com o detector de pontos do dlib e aplica uma transformação afim que leva os cantos dos olhos e o nariz para posições fixas.
3. **Rede:** uma versão reduzida da rede nn4 do FaceNet (a `nn4.small2`, baseada na GoogLeNet), treinada com a *triplet loss*. A saída é um *embedding* de **128 dimensões** sobre a hiperesfera, em que a distância euclidiana mede a semelhança.
4. **Classificação:** para dizer quem é a pessoa, usa um SVM linear sobre os *embeddings*.

O treino usou cerca de **500 mil imagens**, juntando as duas maiores bases públicas da época, CASIA-WebFace e FaceScrub: uma ordem de grandeza menos que o DeepFace e duas menos que o FaceNet.

## Resultados principais

- **92,92% na LFW**, contra 97,35% do DeepFace, 99,64% do FaceNet e 97,53% de humanos (imagens recortadas). O Eigenfaces fica em 60,02%.
- Numa tarefa de classificação entre 10 e 100 pessoas da LFW, o OpenFace teve a maior acurácia por larga margem em comparação com os métodos do OpenCV, e o SVM foi o mais rápido para treinar, o que importa quando é preciso cadastrar pessoas novas.

## Limitações

- A acurácia fica bem abaixo do estado da arte, por causa da base de treino menor.
- Os testes de tempo foram feitos num computador de mesa com CPU Xeon e GPU, não num dispositivo móvel.
- O projeto foi feito em Torch/Lua, uma pilha que hoje caiu em desuso.

## Ligação com o TCC

- **No benchmark, foi o último colocado:** 50,78% com o detector do OpenCV e 51,04% com o RetinaFace. O *recall* foi quase zero (1,6% e 2,6%), o que sugere que o limiar padrão da biblioteca DeepFace não serve para este modelo nas imagens do teste. Mesmo calibrado, dificilmente chegaria perto do ArcFace.
- A motivação do artigo é parecida com a do projeto: reconhecimento facial em dispositivos e IoT, com cadastro rápido de pessoas novas. Vale citar na discussão sobre computação de borda.
- O processo (alinhar, extrair *embedding*, comparar) é o mesmo do software embarcado do projeto.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. Como o OpenFace alinha o rosto antes de passar pela rede?
2. Por que a acurácia do OpenFace na LFW é menor que a do FaceNet, se a ideia é a mesma?
3. O que o *recall* quase zero no benchmark do TCC indica sobre o limiar de decisão?
