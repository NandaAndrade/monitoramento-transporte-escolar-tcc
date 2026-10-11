# Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural

Trabalho de Conclusão de Curso — Escola de Engenharia, UFMG.

**Aluna:** Fernanda Andrade Bicalho da Cruz
**Orientador:** Janier Arias García · **Coorientador:** Frederico Gualberto Ferreira Coelho

## Sobre o projeto

O transporte escolar rural não tem mecanismos automatizados de controle de presença, o que afeta a segurança dos estudantes e a gestão pública. O projeto propõe um dispositivo IoT embarcado em ônibus escolares que:

- identifica e registra a presença dos alunos por **reconhecimento facial (vídeo)** e **reconhecimento de voz (áudio)**;
- envia os dados ao sistema **TRANSCOLAR RURAL** via rede móvel (MQTT/API);
- gera relatórios para gestores escolares e o poder público.

O hardware-alvo é um Raspberry Pi com o AI HAT (acelerador Hailo-10).

| Ciclo | Escopo |
|---|---|
| **TCC I** (ago–nov/2026) | Requisitos, revisão bibliográfica, escolha de algoritmo e hardware, arquitetura, análise de impactos e texto da monografia. |
| **TCC II** | Software embarcado, integração MQTT/API, simulação e teste piloto em ônibus real. |

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `monografia_tcc1.tex`, `referencias.bib`, `assets_tex/` | Texto da monografia do TCC I em LaTeX (ABNT) |
| `monografia/historico/` | Versões anteriores da monografia |
| `Proposta - ... .pdf`, `Projeto de Trabalho de Conclusão de Curso.docx` | Proposta submetida ao colegiado |
| [`Cronograma_Oficial.md`](Cronograma_Oficial.md) | Cronograma consolidado (prevalece sobre a proposta) |
| [`requisitos.md`](requisitos.md) | Requisitos funcionais e não funcionais |
| [`Revisao_Bibliografica_Anotacoes.md`](Revisao_Bibliografica_Anotacoes.md) | Anotações da revisão bibliográfica |
| [`resumo_reconhecimento_facial_tcc.md`](resumo_reconhecimento_facial_tcc.md) | Resumo da exploração de reconhecimento facial |
| [`relatorio_benchmark_reconhecimento_facial.md`](relatorio_benchmark_reconhecimento_facial.md) | Resultados do benchmark de reconhecimento facial |
| `relatorios/` | Relatórios de progresso enviados aos orientadores |
| `preparar_dataset.py` | Baixa e organiza um dataset público de rostos (LFW ou AT&T) |
| `benchmark_face_recognition.py` | Compara 10 modelos de reconhecimento facial via DeepFace |
| `benchmark_resultados.csv`, `benchmark_resultados.png` | Saída do benchmark |
| `dataset/`, `dataset_teste/` | Imagens usadas no benchmark (uma pasta por pessoa) |

## Benchmark de reconhecimento facial

Foram comparados 10 modelos (ArcFace, VGG-Face, Dlib, GhostFaceNet, SFace, FaceNet, FaceNet512, DeepFace, DeepID e OpenFace) no LFW, com 384 pares por modelo. Os destaques:

| Modelo | Acurácia | Tempo médio/par | Tamanho |
|---|---|---|---|
| ArcFace | 92,71% | 0,736 s | 130 MB |
| SFace | 81,51% | 0,089 s | 5 MB |

A tabela completa e a metodologia estão em [`relatorio_benchmark_reconhecimento_facial.md`](relatorio_benchmark_reconhecimento_facial.md).

### Como reproduzir

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install deepface pandas matplotlib opencv-python tf-keras scikit-learn

python preparar_dataset.py --fonte lfw --saida ./dataset
python benchmark_face_recognition.py --dataset_dir ./dataset
```

O modelo "DeepFace" (Facebook) exige TensorFlow ≤ 2.12 e roda num ambiente separado (Python 3.10). Os detalhes estão no relatório do benchmark.

## Compilando a monografia

O texto é editado no Overleaf. Para compilar localmente:

```bash
latexmk -pdf monografia_tcc1.tex
```
