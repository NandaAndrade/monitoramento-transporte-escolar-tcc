# Guia de leitura: GhostFaceNets, reconhecimento facial leve (Alansari *et al.*, 2023)

> **Guia de estudo em português**, não é tradução. O artigo tem licença Creative Commons Atribuição-NãoComercial-SemDerivações 4.0 (CC BY-NC-ND), que não permite distribuir traduções, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** ALANSARI, M.; HAY, O. A.; JAVED, S.; SHOUFAN, A.; ZWEIRI, Y.; WERGHI, N. GhostFaceNets: Lightweight Face Recognition Model From Cheap Operations. *IEEE Access*, v. 11, p. 35429–35446, 2023. DOI 10.1109/ACCESS.2023.3266068.
> **PDF local:** `docs/Referencias/alansari_2023_ghostfacenets.pdf` · **Chave no .bib:** `alansari2023ghostfacenets`

---

## Em uma frase

Os GhostFaceNets são modelos de reconhecimento facial leves, feitos para celulares e sistemas embarcados, que usam os "módulos Ghost" para gerar parte dos mapas de características com operações baratas e chegam a resultados do estado da arte com 60 a 275 MFLOPs.

## O problema

Os modelos de reconhecimento facial mais precisos custam bilhões de operações por imagem, o que é demais para dispositivos com pouca memória e processamento. Os modelos leves anteriores (MobileFaceNets, ShuffleFaceNet, VarGFaceNet) já reduziam esse custo, mas, segundo os autores, não atacavam a **redundância entre os mapas de características**: muitos deles são quase cópias uns dos outros.

## A ideia central

1. **Módulo Ghost:** em vez de calcular todos os mapas de características com convoluções completas, o módulo calcula só uma parte (os mapas "intrínsecos") e gera o resto com transformações lineares baratas. Resultado: quase a mesma informação com bem menos cálculo.
2. **Duas bases de rede:** a GhostNetV1 e a GhostNetV2. A V2 acrescenta um mecanismo de atenção leve, pensado para não atrasar a execução em hardware real, que captura relações entre partes distantes da imagem.
3. **Cabeça de saída adaptada ao rosto:** a última parte da rede foi redesenhada para gerar o *embedding* facial, e a função de ativação usada é a PReLU.
4. **Treino com ArcFace:** os modelos são treinados com a perda do ArcFace, na base MS-Celeb-1M refinada (versões MS1MV2 e MS1MV3).

## Resultados principais

- Custo de **60 a 275 MFLOPs**, conforme a largura da rede e o passo (*stride*) das camadas iniciais. Modelos grandes podem passar de 1.000 MFLOPs.
- O GhostFaceNetV1 treinado na MS1MV3 chegou a **99,73% na LFW** e superou os outros modelos leves em 8 dos 11 testes.
- **Tamanho real abaixo de 13,8 MB** e cerca de **50 ms por imagem** na CPU de um celular com processador ARM, usando o TensorFlow Lite em uma única *thread*.

## Limitações

- As medições de tempo são num celular ARM, não num Raspberry Pi ou num acelerador como o Hailo.
- Todos os testes usam bases públicas de adultos; nada com crianças nem com imagens de câmera de veículo.
- Os resultados dependem de bases de treino enormes (MS-Celeb-1M), que a maioria dos projetos não consegue reproduzir.

## Ligação com o TCC

- **No benchmark, ficou em quarto lugar:** 82,03% com o detector do OpenCV e 81,77% com o RetinaFace, com cerca de 16 MB. Teve precisão de 100% e *recall* baixo (64,1% e 63,5%), padrão que a Visão Geral atribui ao limiar padrão conservador. Depois de calibrar o limiar, pode subir bastante.
- **É o candidato leve mais interessante para o dispositivo.** O artigo mede o modelo com **TensorFlow Lite em processador ARM**, exatamente a pilha prevista para o Raspberry Pi (ver Ferramentas, na Visão Geral). Os 50 ms por imagem no celular sugerem folga em relação à meta de 2 s, mas precisam ser medidos no hardware do projeto.
- Usa a mesma perda do ArcFace, então a diferença entre os dois está na rede, não no treino: é uma troca entre acurácia e custo que vale discutir na escolha do segundo modelo.
- Citado na Visão Geral, na Atividade 1.2 (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. O que o módulo Ghost faz para economizar cálculo?
2. O que a GhostNetV2 acrescenta à V1?
3. Por que as medições de tempo deste artigo são relevantes para o Raspberry Pi, e por que não bastam?
4. O que pode explicar a diferença entre os 99,73% do artigo e os cerca de 82% do benchmark do TCC?
