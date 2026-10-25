# Guia de leitura: CLASSIC, chamada escolar com reconhecimento facial, IoT e computação de borda (Duarte *et al.*, 2025)

> **Guia de estudo em português**, não é tradução. O artigo não traz licença aberta, então este documento resume e explica o conteúdo com outras palavras, para ajudar a ler o original.
>
> **Referência:** DUARTE, M. G.; PEREIRA, M. B.; MATOS, F. de. CLASSIC: Sistema de Chamada Escolar com Reconhecimento Facial através de IoT e Computação de Borda. In: Simpósio Brasileiro de Componentes, Arquiteturas e Reutilização de Software (SBCARS), Recife, 22–26 set. 2025. Páginas e DOI ainda a conferir na SBC OpenLib.
> **PDF local:** `docs/Referencias/duarte_2025_classic_chamada_escolar_iot_borda.pdf` · **Chave no .bib:** `duarte2025classic`

---

## Em uma frase

Um terminal com Raspberry Pi e câmera que faz a chamada em sala de aula por reconhecimento facial com a biblioteca DeepFace e, quando há um computador mais potente na rede local, transfere para ele o reconhecimento (*offloading*) para responder mais rápido.

## O sistema

1. **Hardware:** Raspberry Pi 4B (4 GB) com câmera OV5647 de 5 MP e um visor LCD1602 que orienta o aluno e mostra o resultado, tudo numa caixa impressa em 3D. O "dispositivo de borda" é um notebook com Core i5-12450H e 24 GB de RAM.
2. **Fluxo em três fases:** aquisição da imagem (só captura quando há rosto), reconhecimento e registro da frequência em SQLite.
3. **Dois modos de reconhecimento:**
   - **local:** o próprio Raspberry Pi roda todo o pipeline;
   - **remoto:** na inicialização, o Pi procura um servidor de borda na rede local e, se encontrar, envia as imagens por gRPC. Se o servidor cair, o sistema volta sozinho para o modo local.
4. **Software:** Python 3.12, OpenCV para detecção e DeepFace para reconhecimento, que dispensa treinar um modelo próprio.

## Escolha do modelo

- Os autores testaram combinações de detector e modelo do DeepFace num conjunto de 98 pessoas com 12 imagens cada (Tabela 2 do artigo). As combinações com **ArcFace** ficaram no topo: 98% com YOLOv8 ou MTCNN, 96% com RetinaFace.
- Mesmo assim, usaram **SSD + ArcFace** (90%), porque as combinações melhores exigiam dependências que não conseguiram instalar no prazo.

## Resultados

- **Teste real:** 14 voluntários num laboratório, com o dispositivo a 1,5 m de altura e iluminação mista. O sistema acertou 12 dos 14 alunos (**85,71%**) nos dois modos.
- **Tempo:** **4,5 s** por reconhecimento no Raspberry Pi e **1,97 s** com o servidor de borda (56% menos).
- **Teste de estresse:** simulação de até 25 salas com 50 alunos cada, enviando pedidos simultâneos ao servidor de borda. A acurácia ficou perto de 84% em todas as cargas; o tempo médio passou de 1,4 s (1 sala) para 3,7 s (5 salas) e 34 s (25 salas).

## Limitações (apontadas pelos autores e outras)

- Poucos participantes (14) e ambiente interno com iluminação controlada.
- Óculos e chapéus causaram erros de reconhecimento.
- Reconhece um aluno por vez, que precisa ficar parado diante do visor.
- **Todas as imagens capturadas foram armazenadas** para os testes de estresse; o artigo não discute privacidade nem LGPD.
- O modo rápido depende de um computador na mesma rede Wi-Fi.
- A acurácia relatada vem do mesmo pequeno grupo, sem separar falso positivo de falso negativo.

## Ligação com o TCC

- É o trabalho correlato **mais parecido com o projeto em pilha de software**: Raspberry Pi, DeepFace (cita o mesmo Serengil e Ozpinar, 2020) e ArcFace. É brasileiro e recente.
- **Confirma o benchmark do TCC:** o ArcFace também foi o melhor modelo para eles, e a acurácia com RetinaFace (96%) é próxima dos 96,61% do benchmark.
- **Justifica o acelerador:** 4,5 s no Raspberry Pi 4 sem acelerador está bem acima da meta de 2 s, o que reforça a escolha do Raspberry Pi 5 com o AI HAT (Hailo) na Atividade 1.3.
- **Ilustra a limitação "benchmark ≠ uso real":** a acurácia caiu de 90–98% nos testes com imagens para 85,7% com pessoas reais, num cenário ainda mais fácil que a porta de um ônibus.
- **Diferenças a destacar na comparação:**
  - o projeto não guarda nenhuma imagem; o CLASSIC guarda todas;
  - o projeto faz tudo no próprio dispositivo e lida com a rede instável por uma fila local; o CLASSIC depende de um servidor na rede local para ser rápido;
  - o projeto reconhece o aluno passando pela porta, sem pedir que ele pare ou se posicione;
  - o retorno ao motorista é por LED e bipe, sem tela.
- Citado na Visão Geral, no parágrafo de trabalhos correlatos (`visao_geral.tex`).

## Perguntas para conferir a leitura

1. O que muda entre o modo local e o modo remoto do CLASSIC, e o que acontece se o servidor de borda cair?
2. Por que os autores usaram SSD + ArcFace se outras combinações tiveram acurácia maior?
3. Quais números do artigo justificam usar um acelerador no Raspberry Pi do projeto?
4. Qual a diferença entre o CLASSIC e o projeto no tratamento das imagens dos alunos, e por que isso importa para a LGPD?
