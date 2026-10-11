# Monitoramento de Presença em Transporte Escolar Rural

Sistema IoT embarcado em ônibus escolares que registra a presença dos alunos por **reconhecimento facial (vídeo)** e **reconhecimento de voz (áudio)** e envia os dados para um sistema de gestão via rede móvel (MQTT/API).

O hardware-alvo é um Raspberry Pi com o AI HAT (acelerador Hailo-10).

## Benchmark de reconhecimento facial

Para escolher o modelo de reconhecimento facial, foram comparados 10 modelos disponíveis na biblioteca [DeepFace](https://github.com/serengil/deepface): ArcFace, VGG-Face, Dlib, GhostFaceNet, SFace, FaceNet, FaceNet512, DeepFace, DeepID e OpenFace.

- **Dataset:** LFW (Labeled Faces in the Wild), 96 pessoas com pelo menos 15 fotos cada
- **Pares avaliados por modelo:** 384 (192 da mesma pessoa e 192 de pessoas diferentes)
- **Detector de rosto:** OpenCV (Haar Cascade), o mais leve, pensando no uso embarcado

| # | Modelo | Acurácia | Precisão | Recall | F1 | Tempo médio/par (s) | Tamanho (MB) |
|---|---|---|---|---|---|---|---|
| 1 | **ArcFace** | **92,71%** | 99,40% | 85,94% | 0,9218 | 0,736 | 130 |
| 2 | VGG-Face | 88,02% | 96,79% | 78,65% | 0,8678 | 2,379 | 580 |
| 3 | Dlib | 84,90% | 99,26% | 70,31% | 0,8232 | 1,247 | 22 |
| 4 | GhostFaceNet | 82,55% | 100% | 65,10% | 0,7886 | 0,664 | 16 |
| 5 | SFace | 81,51% | 100% | 63,02% | 0,7732 | **0,089** | 5 |
| 6 | Facenet | 76,04% | 100% | 52,08% | 0,6849 | 1,104 | 90 |
| 7 | Facenet512 | 72,66% | 100% | 45,31% | 0,6237 | 0,845 | 90 |
| 8 | DeepFace (Facebook) | 60,94% | 73,33% | 34,38% | 0,4681 | 12,949 | 150 |
| 9 | DeepID | 51,56% | 80,00% | 4,17% | 0,0792 | 0,071 | 3 |
| 10 | OpenFace | 50,78% | 100% | 1,56% | 0,0308 | 0,303 | 30 |

Resultados completos em [`benchmark_resultados.csv`](benchmark_resultados.csv) e [`benchmark_resultados.png`](benchmark_resultados.png). A análise detalhada está em [`relatorio_benchmark_reconhecimento_facial.md`](relatorio_benchmark_reconhecimento_facial.md).

### Como reproduzir

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install deepface pandas matplotlib opencv-python tf-keras scikit-learn

python preparar_dataset.py --fonte lfw --saida ./dataset
python benchmark_face_recognition.py --dataset_dir ./dataset
```

- `preparar_dataset.py` baixa um dataset público de rostos (`--fonte lfw` ou `--fonte att`) e organiza as imagens em uma pasta por pessoa.
- `benchmark_face_recognition.py` gera os pares, roda cada modelo em um processo isolado e salva o CSV e o gráfico. Outras opções: `--pares_por_pessoa` e `--detector_backend` (`opencv`, `retinaface`, `mtcnn`, `yunet`...).

O modelo "DeepFace" (Facebook) exige TensorFlow ≤ 2.12, então roda num ambiente separado com Python 3.10.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `preparar_dataset.py` | Download e organização do dataset |
| `benchmark_face_recognition.py` | Benchmark dos modelos de reconhecimento facial |
| `benchmark_resultados.csv`, `benchmark_resultados.png` | Saída do benchmark |
| `dataset/`, `dataset_teste/` | Imagens usadas no benchmark (uma pasta por pessoa) |
| [`requisitos.md`](requisitos.md) | Requisitos funcionais e não funcionais do sistema |
