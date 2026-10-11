# Reconhecimento Facial para o TCC — Resumo da Conversa

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Escopo desta conversa:** parte de **reconhecimento facial** (vídeo) — levantamento de algoritmos candidatos, trade-offs para hardware embarcado, metodologia de teste e scripts de benchmark.

> **Status:** este documento registra o **planejamento** original (levantamento de algoritmos, metodologia, scripts na versão inicial). O benchmark já foi **executado de ponta a ponta** contra o dataset LFW, incluindo os 10 algoritmos planejados. Para os **resultados reais** e para as versões atuais (e corrigidas) dos scripts, ver [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md), [benchmark_reconhecimento_facial.py](../pesquisa/benchmark_reconhecimento_facial.py) e [benchmark_resultados.csv](../pesquisa/resultados/benchmark_resultados.csv). As seções abaixo foram mantidas como registro histórico da etapa de planejamento; onde o código ou os números embutidos aqui divergem do que foi de fato executado, prevalece o relatório de resultados.
>
> **Reorganização (2026-10-11):** os scripts citados abaixo estão em [`pesquisa/`](../pesquisa/). `benchmark_face_recognition.py` virou `pesquisa/benchmark_reconhecimento_facial.py`, e os datasets `dataset/` e `dataset_teste/` viraram `pesquisa/dados/lfw/` e `pesquisa/dados/att/`.

---

## 1. Contexto e restrições do projeto

- Hardware considerado: **Raspberry Pi** (com acelerador **Hailo AI HAT**, Hailo-8/8L ou Hailo-10H) vs. **ESP32** — decisão a ser formalizada na Atividade 1.3 (Projeto Arquitetural e Análise de Trade-offs).
- Condições reais de uso: câmera dentro de um ônibus escolar rural — iluminação variável, vibração, ângulos não controlados, possível baixa resolução.
- Restrição legal: dados de **alunos menores de idade** — LGPD será tratada formalmente na Atividade 1.4, então **nesta fase de prototipagem não se deve usar fotos reais de alunos**.
- Foi observado (via pesquisa) que o Hailo-8L já tem relatos de rodar modelos como RetinaFace para detecção facial, e que os HATs suportam modelos convertidos para ONNX/HEF — o que reforça a viabilidade de um pipeline **detector leve + reconhecedor leve** rodando na NPU em vez do CPU do Pi.

---

## 2. Os 10 algoritmos de reconhecimento facial avaliados

Todos os 10 são acessíveis através de uma única biblioteca Python (`DeepFace`), que já embala esses backbones atrás de uma API comum — permitindo testar todos com o mesmo pipeline de detecção/alinhamento, de forma justa e comparável.

| # | Algoritmo | Tipo / origem | Tamanho aprox. | Acurácia (LFW)* | Embarcável? | Observação |
|---|---|---|---|---|---|---|
| 1 | **VGG-Face** | CNN profunda (Oxford, 2015) | ~500 MB | ~98,8% | Fraco | Pesado demais para Pi/Hailo sem otimização |
| 2 | **FaceNet (128d)** | Google, 2015 (triplet loss) | ~90 MB | ~99,2% | Médio | Roda em CPU do Pi, mas com latência |
| 3 | **FaceNet512** | Variante 512d | ~90 MB | ~99,6% | Médio | Mais preciso que o 128d, mesmo custo |
| 4 | **OpenFace** | Leve, CMU | ~30 MB | ~93,8% | Bom | Rápido, mas perde muita acurácia |
| 5 | **DeepFace (Facebook)** | Original 2014, alinhamento 3D | Pesado | ~97,4% | Fraco | Mais histórico/comparativo que prático hoje |
| 6 | **DeepID** | 2014, embeddings pequenos | Leve | ~97,5% | Médio | Arquitetura antiga, pouco mantida |
| 7 | **ArcFace** | Loss angular (additive margin), 2019 | Variável (leve com backbone MobileFaceNet) | ~99,8% (99,55% na variante MobileFaceNet de 4 MB) | **Ótimo** (na variante leve) | Melhor relação acurácia/tamanho da lista |
| 8 | **Dlib (ResNet-29)** | HOG + ResNet pequena | ~22 MB | ~99,4% | Bom | Muito usado via `face_recognition`, fácil de prototipar |
| 9 | **SFace** | OpenCV Zoo, focado em condições reais | Muito leve (ONNX nativo) | ~99,0% (mais robusto em imagens degradadas/baixa resolução) | **Ótimo** | Não depende de TensorFlow/PyTorch — só OpenCV DNN, ideal para o Pi |
| 10 | **GhostFaceNet** | Ghost modules (mobile-first), 2023 | Muito leve | ~99,7% | **Ótimo** | Projetado explicitamente para edge devices |

\*valores de acurácia são os reportados na literatura/documentação de cada modelo no benchmark LFW (condições controladas). Em condições reais (dentro de um ônibus), os números tendem a cair — por isso o **SFace** se destaca: estudos mostram que ele mantém acurácia mais estável em condições degradadas/vigilância do que ArcFace/FaceNet, que são otimizados para cenas controladas.

**Bônus citável na revisão bibliográfica (11º/12º candidato):**
- **MobileFaceNet** — ArcFace treinado com backbone móvel, 4 MB, 99,55% no LFW.
- **Buffalo_L / InsightFace** — ~99,83% no LFW, backbone ResNet50 (mais pesado que os "leves" acima).

**Conclusão preliminar de trade-off:** o caminho mais realista para o hardware do projeto é **detector leve (YuNet ou RetinaFace) + reconhecedor leve (SFace, GhostFaceNet ou ArcFace/MobileFaceNet)**. ESP32 puro não tem RAM/CPU suficiente para rodar qualquer uma dessas redes com qualidade aceitável — reforça a escolha por Raspberry Pi + Hailo.

---

## 3. Metodologia de teste proposta

1. Montar um dataset com pastas por pessoa (mínimo 2 fotos por pessoa, idealmente mais).
2. Gerar pares positivos (mesma pessoa) e negativos (pessoas diferentes).
3. Rodar `DeepFace.verify()` para os 10 modelos, medindo: acurácia, precisão, recall, F1 e tempo médio de inferência por par.
4. Comparar os resultados em CSV/gráfico e escolher os **2 melhores** considerando **acurácia E viabilidade de embarque** (não só acurácia isolada — tamanho do modelo e tempo de inferência pesam tanto quanto).

---

## 4. Datasets recomendados para os testes

| Dataset | O que é | Nº pessoas / fotos | Condições | Uso recomendado |
|---|---|---|---|---|
| **LFW** (Labeled Faces in the Wild) | Padrão-ouro acadêmico para reconhecimento facial | 5.749 pessoas / 13.233 fotos (poucas com muitas fotos cada — filtrar por mínimo) | Iluminação, ângulo e fundo variados — mais parecido com o desafio real | **Recomendado para os resultados que vão para a monografia** — é o benchmark citado na maioria dos papers sobre ArcFace/SFace/GhostFaceNet |
| **AT&T / Olivetti Faces** | Dataset clássico de laboratório (Cambridge) | 40 pessoas × 10 fotos | Fundo escuro uniforme, iluminação de estúdio, preto e branco | Só para **testar rapidamente se o pipeline está funcionando** — documentação oficial avisa que é "pequeno, antigo e não deve ser usado para publicar resultados científicos" |

Ambos são de **adultos que consentiram participar de pesquisa acadêmica pública** — adequado para esta fase, sem tocar em dados de alunos menores de idade. Se precisar de mais volume/diversidade depois, considerar **VGGFace2** ou o dataset **"Pins Face Recognition"** do Kaggle (mais imagens por pessoa, mais variação de ângulo — exige conta/API do Kaggle).

---

## 5. Scripts criados

> Os dois scripts abaixo foram **implementados, executados e desde então corrigidos** — o código evoluiu no repositório depois da conversa que gerou este planejamento. Em vez de manter uma segunda cópia (que ficaria desatualizada), esta seção descreve o que cada script faz e aponta para o arquivo real; **use sempre [preparar_dataset.py](../pesquisa/preparar_dataset.py) e [benchmark_reconhecimento_facial.py](../pesquisa/benchmark_reconhecimento_facial.py) do repositório como fonte da verdade**, não o texto abaixo.
>
> Principais mudanças desde a versão originalmente planejada aqui (detalhadas em [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md)):
> - Cada modelo agora roda em **processo isolado** (`multiprocessing`, flag `--sem_isolamento` para desativar) — sem isso, o tempo de inferência de modelos avaliados por último ficava artificialmente inflado pelos modelos anteriores ainda residentes em memória (o SFace chegou a aparecer 47x mais lento do que realmente é).
> - `opencv-python` precisa estar fixado em `==4.10.0.84` — a versão mais recente do PyPI (5.0.0) não inclui os arquivos de cascata Haar e quebra o detector `opencv` silenciosamente.

### 5.1 `preparar_dataset.py`

Baixa um dataset público de rostos (LFW ou AT&T/Olivetti) via `scikit-learn` — sem precisar de link manual — e organiza as imagens na estrutura de pastas esperada pelo script de benchmark (`dataset/pessoa_XX/foto.jpg`). Código completo: [preparar_dataset.py](../pesquisa/preparar_dataset.py).


### 5.2 `benchmark_face_recognition.py`

Roda os 10 algoritmos (via `DeepFace`) sobre o dataset preparado, calcula acurácia/precisão/recall/F1 e tempo médio de inferência, e gera um CSV + gráfico comparativo.


---

## 6. Fluxo de uso completo (rodar na sua máquina)

```bash
pip install scikit-learn pillow deepface pandas matplotlib "opencv-python==4.10.0.84" tf-keras

# 1) baixa e organiza o dataset
python preparar_dataset.py --fonte lfw --min_fotos_por_pessoa 15 --saida ./dataset

# 2) roda o benchmark (por padrao, isola cada modelo em um processo)
python benchmark_face_recognition.py --dataset_dir ./dataset
```

> Fixe `opencv-python` em `4.10.0.84` — a versão mais recente do PyPI (5.0.0) não inclui os arquivos de cascata Haar e quebra o detector `opencv` silenciosamente (todos os pares dão erro sem mensagem clara). O `Dlib` e o modelo `DeepFace` (Facebook) exigem passos extras não cobertos neste fluxo básico — ver seção 3 de [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md).

---

## 7. Próximos passos sugeridos

- ~~Rodar o benchmark e interpretar os resultados junto com a orientação.~~ **Concluído** — ver [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md): ArcFace (92,71%) e SFace (mais rápido, 0,089s/par) recomendados.
- Testar a etapa de **detecção** separadamente (YuNet vs RetinaFace vs MTCNN), já que a acurácia final depende dos dois estágios (detecção + reconhecimento). **Parcialmente concluído** — RetinaFace × OpenCV comparados em 05/10/2026 (ver seção 7 de [benchmark_reconhecimento_facial.md](benchmark_reconhecimento_facial.md)): ArcFace sobe para 96,61% e VGG-Face para 95,57%, mas SFace não melhora. YuNet e MTCNN ainda pendentes.
- Escrever a seção de Revisão Bibliográfica (Atividade 1.2) da monografia com base nessa comparação, citando as fontes corretamente. **Em andamento** — [monografia_tcc1.tex](../monografia/monografia_tcc1.tex) já tem a subseção sobre Eigenfaces/Fisherfaces/LBPH (por que ficaram de fora do benchmark); a comparação empírica completa dos 10 modelos ainda não foi redigida em prosa acadêmica.
- Se o LFW se mostrar pequeno demais, considerar VGGFace2 ou "Pins Face Recognition" (Kaggle) para mais volume/diversidade. **Ainda pendente** — não avaliado nesta rodada.
