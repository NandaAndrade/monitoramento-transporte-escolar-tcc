# Anotações Técnicas para Revisão Bibliográfica

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Aluna:** Fernanda Andrade Bicalho da Cruz
**Última atualização:** 2026-10-11

> Documento vivo — atualizado ao longo das conversas de estudo, para servir de base à seção de Revisão Bibliográfica do TCC I (Atividade 1.2) e às decisões de arquitetura (Atividade 1.3).

---

## 1. Contexto do projeto (referência rápida)

- **Hardware em avaliação (trade-off ainda aberto):** Raspberry Pi vs. microcontrolador ESP32
- **Periféricos:** câmera HD, microfone direcional
- **Stack de software definida:** Python, OpenCV, TensorFlow Lite, MQTT, Node.js
- **Banco de dados em avaliação:** PostgreSQL ou Firebase
- **Meta de desempenho:** acurácia >90% no reconhecimento de presença, baixa latência
- **Restrições:** alimentação veicular, ambiente com vibração/iluminação variável, LGPD (dados de menores)

---

## 2. TensorFlow

Biblioteca open source de machine learning/deep learning, criada pelo Google (2015).

- **Tensor**: generalização de array multidimensional (escalar, vetor, matriz, ...). Todos os dados (imagem, áudio, texto) viram tensores.
- **Flow**: fluxo dos tensores por um grafo computacional de operações; o framework calcula gradientes automaticamente (backpropagation) para treinar.
- **Keras**: API de alto nível usada hoje na prática para montar modelos por camadas (`Dense`, `Conv2D`, `LSTM`, etc.), sem manipular tensores manualmente.
- **Uso típico**: construir e treinar redes neurais (CNNs, RNNs, Transformers) usando GPU/TPU, depois exportar para produção (servidor, mobile via **TensorFlow Lite**, navegador via TensorFlow.js).
- **Concorrente principal**: PyTorch (Meta). Diferença histórica (TF = produção, PyTorch = pesquisa) hoje bem diluída.
- **Relevância para o projeto**: o projeto já define **TensorFlow Lite** como parte da stack — é a versão otimizada do TensorFlow para dispositivos embarcados/edge (baixo consumo de memória e CPU), adequada para Raspberry Pi e, em menor grau, ESP32.

---

## 3. OpenCV

Biblioteca open source de **visão computacional** e processamento de imagem/vídeo, originada na Intel (1999). Escrita em C++, com bindings para Python (mais usado), Java, etc.

- **Funcionalidades principais**: manipulação básica de imagem (resize, crop, filtros), detecção de bordas/contornos (Canny, Sobel), detecção clássica de objetos (Haar Cascades, Hough Transform), rastreamento de movimento, calibração de câmera, leitura/escrita de imagem e vídeo (webcam, arquivos).
- **Papel no pipeline de deep learning**: OpenCV cuida do **pré-processamento** (captura, corte, normalização) e **pós-processamento** (desenhar bounding boxes, extrair ROI); o modelo de deep learning (TensorFlow/TFLite) cuida da inferência propriamente dita.
  ```
  Captura (OpenCV) → pré-processamento (OpenCV) → inferência (TensorFlow Lite) → pós-processamento (OpenCV)
  ```
- **Relevância para o projeto**: já definido na stack (Atividade 1.2 do cronograma cita "técnicas de reconhecimento facial (OpenCV)"). OpenCV também tem módulo de DNN (`cv2.dnn`) capaz de rodar modelos de detecção facial nativamente, incluindo o YuNet (ver seção 4).

---

## 4. Detecção facial: RetinaFace vs. YuNet

Ambos são modelos de **detecção** facial (localizam o rosto na imagem — bounding box + 5 landmarks), **não** de reconhecimento/identificação. Para identificar *qual* aluno é, é necessário um segundo modelo de reconhecimento (embedding facial), como ArcFace, SFace ou FaceNet, que compara o rosto detectado com um banco de rostos cadastrados.

### RetinaFace
- Publicado em 2019 pelo time do InsightFace (mesmo grupo do ArcFace). Foco em **precisão**.
- Arquitetura: Feature Pyramid Network (FPN) + módulos de contexto sobre backbone (ResNet50 "grande" ou MobileNet0.25 "leve"); multitarefa (bounding box + 5 landmarks + regressão 3D densa como supervisão auxiliar).
- Ponto forte: robustez em rostos pequenos, ocluídos ou em ângulos difíceis (referência no benchmark WIDER FACE).
- Ponto fraco: mais pesado computacionalmente; sem integração nativa no OpenCV — requer ONNX Runtime ou a lib `insightface` como dependência extra.

### YuNet
- Desenvolvido pelo laboratório de Shiqi Yu; adotado como detector facial padrão do **OpenCV** (`cv2.FaceDetectorYN`, desde OpenCV 4.5.4+).
- Foco em **eficiência**: modelo muito leve (~75-100 KB), arquitetura anchor-free, pensado para CPU/edge/mobile em tempo real.
- Também retorna 5 landmarks faciais.
- Ponto fraco: um pouco menos robusto que RetinaFace em casos extremos (rostos minúsculos, ângulos muito difíceis).

### Comparativo

| | RetinaFace | YuNet |
|---|---|---|
| Foco | Precisão | Velocidade/leveza |
| Tamanho do modelo | Maior (MBs) | Muito pequeno (KBs) |
| Robustez a casos difíceis | Melhor | Boa, mas inferior |
| Integração com OpenCV | Não nativa (ONNX/insightface) | Nativa (`cv2.FaceDetectorYN_create`) |
| Uso típico | Pipelines de alta acurácia (ex: com ArcFace) | Tempo real, edge devices |

### Compatibilidade com o projeto

- Ambos são **compatíveis em princípio** (open source, adaptáveis a Python/OpenCV/TFLite), mas com ajuste de expectativa: são apenas o estágio de *detecção*, não de *identificação* — o pipeline completo precisa de um modelo de reconhecimento adicional.
- **Hardware**: nenhum dos dois é viável em ESP32 "puro" (microcontrolador, ~320-520 KB RAM, sem SO completo) na forma padrão — famílias de projetos de detecção facial em ESP32 (ex: `ESP-WHO` da Espressif) usam redes drasticamente menores (variantes reduzidas de MTCNN). Isso é um argumento a favor do **Raspberry Pi** na análise de trade-off da Atividade 1.3.
- **YuNet** se encaixa melhor na stack já definida: integração nativa com OpenCV (zero dependência extra), leve o suficiente para Raspberry Pi com baixa latência — bom para a meta de não travar o embarque/desembarque dos alunos.
- **RetinaFace** seria justificável se testes empíricos mostrarem que as condições reais do ônibus (ângulo de entrada, contraluz, movimento) degradam demais a acurácia do YuNet, já que é mais robusto nesses cenários difíceis — ao custo de mais peso computacional e complexidade de integração (conversão para ONNX/TFLite).

### Decisão em aberto para o TCC
- [ ] Citar ambos os modelos na revisão bibliográfica (Atividade 1.2) como parte da análise de trade-off de detecção facial.
- [ ] Decisão final entre RetinaFace e YuNet fica para o TCC II, após testes empíricos de acurácia e tempo de resposta no hardware escolhido.
- [x] ~~Ainda em aberto: modelo de **reconhecimento** facial (segunda etapa do pipeline) a ser usado em conjunto com o detector — candidatos a pesquisar: ArcFace, SFace.~~ **Resolvido empiricamente (ver seção 5 abaixo).**

---

## 5. Reconhecimento facial: benchmark empírico dos 10 candidatos

Os 10 algoritmos de reconhecimento (segunda etapa do pipeline, depois da detecção discutida na seção 4) foram implementados via biblioteca `DeepFace` e testados contra 384 pares de imagens do dataset LFW. Resultado completo em [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md) e [benchmark_resultados.csv](../pesquisa/resultados/benchmark_resultados.csv).

**Ranking por acurácia:** ArcFace (92,71%) > VGG-Face (88,02%) > Dlib (84,90%) > GhostFaceNet (82,55%) > SFace (81,51%) > Facenet (76,04%) > Facenet512 (72,66%) > DeepFace/Facebook (60,94%) > DeepID (51,56%) > OpenFace (50,78%).

**Recomendação para o hardware do projeto:** **ArcFace** (melhor acurácia, tempo de inferência aceitável) + **SFace** (mais leve em disco — 5 MB — e o mais rápido de todos após corrigir uma distorção de medição causada por rodar vários modelos TensorFlow no mesmo processo; ver relatório para detalhes). GhostFaceNet segue como alternativa leve de reserva.

**Achado metodológico relevante:** o `DeepFace` (a biblioteca) nunca libera da memória um modelo já carregado, então medir o tempo de inferência de vários modelos no mesmo processo Python distorce os resultados dos últimos da fila (chegou a fazer o SFace parecer 47x mais lento do que é). O script de benchmark foi corrigido para isolar cada modelo em um processo separado.

**Detector — RetinaFace testado (05/10/2026):** o benchmark foi repetido com `retinaface` no lugar do `opencv`/Haar Cascade (seção 4). ArcFace (96,61%) e VGG-Face (95,57%) passam a superar a meta de 90%; Facenet/Facenet512 melhoram um pouco; SFace, GhostFaceNet e Dlib não mudam, e DeepID/OpenFace continuam perto de 50%. O preço é o tempo: ~0,62 s de detecção por imagem em CPU, contra ~0,02 s do Haar. Detalhes na seção 7 do [relatório](benchmark_reconhecimento_facial.md). **Ainda pendente:** testar o `yunet`.

**Algoritmos citados na literatura mas fora do benchmark empírico:**
- MobileFaceNet e InsightFace/Buffalo_L — variantes/origem do próprio ArcFace já testado, não algoritmos concorrentes distintos.
- MediaPipe Face Detection e S3FD — são detectores, não reconhecedores; pertencem à discussão da seção 4, não a esta.
- Eigenfaces, Fisherfaces e LBPH — métodos clássicos pré-deep-learning, mencionados na monografia como marco histórico, mas fora do benchmark por não estarem disponíveis na biblioteca `DeepFace` e por serem, segundo a literatura, muito sensíveis às condições de iluminação/ângulo esperadas no ônibus escolar.

---

## Histórico de tópicos discutidos
- 2026-09-16: TensorFlow (visão geral)
- 2026-09-16: OpenCV (visão geral)
- 2026-09-16: RetinaFace vs. YuNet (comparação e compatibilidade com o projeto)
- 2026-09-16: Benchmark empírico dos 10 algoritmos de reconhecimento facial contra o dataset LFW; correção de uma distorção de medição de tempo (isolamento de processo); Dlib e DeepFace/Facebook viabilizados; discussão sobre MobileFaceNet, InsightFace, MediaPipe, S3FD, LBPH e Eigenfaces/Fisherfaces
- 2026-10-05: Benchmark repetido com o detector RetinaFace (comparação OpenCV × RetinaFace nos mesmos 384 pares)
