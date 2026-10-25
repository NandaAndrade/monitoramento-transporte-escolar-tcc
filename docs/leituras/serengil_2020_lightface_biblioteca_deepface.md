# Guia de leitura: LightFace, a biblioteca DeepFace (Serengil e Ozpinar, 2020)

> **Guia de estudo em português**, não é tradução. O artigo é protegido por direitos autorais (IEEE), então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** SERENGIL, S. I.; OZPINAR, A. LightFace: a hybrid deep face recognition framework. In: INNOVATIONS IN INTELLIGENT SYSTEMS AND APPLICATIONS CONFERENCE (ASYU), 2020. *Proceedings* [...]. IEEE, 2020. p. 23–27. DOI: [10.1109/ASYU50717.2020.9259802](https://doi.org/10.1109/ASYU50717.2020.9259802) · biblioteca: [github.com/serengil/deepface](https://github.com/serengil/deepface).
> **PDF local:** `Downloads/Referencias/serengil_2020_lightface_biblioteca_deepface.pdf` · **Chave no .bib:** `serengil2020lightface`

---

## Em uma frase

O artigo apresenta a biblioteca Python hoje chamada **DeepFace**, que junta vários modelos de reconhecimento facial atrás de uma interface única e executa o pipeline completo (detectar, alinhar, representar e verificar) em poucas linhas.

## O que o artigo traz

1. **Uma revisão curta do pipeline de reconhecimento facial**, em quatro etapas:
   - **detecção:** achar o rosto na imagem;
   - **alinhamento:** girar e recortar o rosto para que os olhos fiquem na horizontal;
   - **representação:** passar o rosto pela rede e obter o *embedding*;
   - **verificação:** comparar dois *embeddings* com uma distância e um limiar.
   Os autores observam que a maioria dos artigos só fala da etapa de representação, embora as outras pesem no resultado. Citam, por exemplo, que no FaceNet o alinhamento elevou a acurácia na LFW de 98,87% para 99,63%.
2. **A arquitetura "híbrida" da biblioteca:** o usuário escolhe o modelo (VGG-Face, FaceNet, OpenFace, DeepFace do Facebook, entre outros, na versão do artigo) e a métrica de distância (cosseno, euclidiana ou euclidiana com vetores normalizados), sem mudar o resto do código.
3. **Como os limiares foram definidos:** os autores rodaram os modelos em uma base de pares e usaram uma árvore de decisão (algoritmo C4.5) para achar, para cada combinação de modelo e métrica, o valor de distância que melhor separa "mesma pessoa" de "pessoas diferentes". Esses são os **limiares padrão** da biblioteca.
4. Tabelas com acurácia, precisão, *recall* e F1 de cada combinação de modelo e métrica nesses limiares.

## Limitações

- É um artigo de ferramenta, curto, sem avaliação nos protocolos oficiais (como a View 2 da LFW).
- Os limiares padrão foram ajustados em uma base específica; em outra base ou com outro detector, podem não ser os melhores.
- A biblioteca evoluiu muito depois do artigo (mais modelos e detectores); a versão usada no projeto (0.0.101) é bem diferente da descrita.

## Ligação com o TCC

- **Deve ser citado sempre que os números do benchmark aparecerem**, porque todos vieram desta biblioteca.
- Justifica a escolha metodológica: com o mesmo pipeline para todos os modelos, a comparação entre eles é justa.
- **Ponto crítico:** o benchmark usou os limiares padrão da biblioteca, definidos pelos autores em outra base. Isso ajuda a explicar o padrão "precisão alta e *recall* baixo" de vários modelos e reforça a necessidade de calibrar o limiar na própria base do projeto (item M2 do [documento de lacunas](../lacunas_revisao_bibliografica.md)).
- O artigo também dá a base para descrever o pipeline de quatro etapas na monografia.

## Perguntas para conferir a leitura

1. Quais são as quatro etapas do pipeline e qual delas os artigos costumam ignorar?
2. Como os limiares padrão do DeepFace foram escolhidos, e por que isso importa para os resultados do projeto?
3. Por que usar uma biblioteca única deixa a comparação entre modelos mais justa?
