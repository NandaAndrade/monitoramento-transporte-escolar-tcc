# Reconhecimento Facial para o TCC — Resumo da Conversa

**Projeto:** Sistema IoT para Monitoramento da Presença de Estudantes em Transporte Escolar Rural por Reconhecimento de Voz e Vídeo
**Escopo desta conversa:** parte de **reconhecimento facial** (vídeo) — levantamento de algoritmos candidatos, trade-offs para hardware embarcado, metodologia de teste e scripts de benchmark.


> **Nota (reorganização de 2026-10-11):** este é um registro da conversa original. Os scripts citados agora estão em [`pesquisa/`](../pesquisa/), com outros nomes e código atualizado: `benchmark_face_recognition.py` virou `pesquisa/benchmark_reconhecimento_facial.py`, e os datasets `dataset/` e `dataset_teste/` viraram `pesquisa/dados/lfw/` e `pesquisa/dados/att/`.

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

### 5.1 `preparar_dataset.py`

Baixa um dataset público de rostos (LFW ou AT&T/Olivetti) via `scikit-learn` — sem precisar de link manual — e organiza as imagens na estrutura de pastas esperada pelo script de benchmark (`dataset/pessoa_XX/foto.jpg`).

```python
"""
preparar_dataset.py - TCC: reconhecimento facial para presenca em transporte escolar

Baixa um dataset PUBLICO de rostos (via scikit-learn, sem precisar de link
manual) e organiza as imagens na estrutura de pastas esperada pelo
benchmark_face_recognition.py:

    dataset/
        pessoa_00/
            foto_0000.jpg
            foto_0001.jpg
        pessoa_01/
            ...

Fontes disponiveis:
    lfw -> Labeled Faces in the Wild (recomendado para os resultados do TCC:
           e o benchmark padrao usado na maioria dos papers de ArcFace/SFace/
           GhostFaceNet etc., com condicoes variadas de luz/angulo/fundo).
    att -> AT&T / Olivetti Faces (dataset pequeno e controlado, 40 pessoas x
           10 fotos cada. Use SO para validar rapidamente se o pipeline de
           benchmark esta funcionando - a documentacao oficial avisa que
           e antigo demais para basear resultados publicados nele).

Ambos os datasets sao de adultos que consentiram participar de pesquisa
academica publica - adequado para esta fase de prototipagem, sem usar
dados de alunos menores de idade.

------------------------------------------------------------------------
INSTALACAO (rodar na sua maquina, nao dentro do ambiente do Claude):
    pip install scikit-learn pillow

USO:
    # Dataset "de verdade", citavel na monografia
    python preparar_dataset.py --fonte lfw --min_fotos_por_pessoa 15 --saida ./dataset

    # Teste rapido so para validar o pipeline
    python preparar_dataset.py --fonte att --saida ./dataset_teste

Depois de gerado, rode:
    python benchmark_face_recognition.py --dataset_dir ./dataset
------------------------------------------------------------------------
"""

import argparse
import os

from PIL import Image


def salvar_pessoas(imagens, rotulos, nomes, saida_dir):
    os.makedirs(saida_dir, exist_ok=True)
    for idx, (img, rotulo) in enumerate(zip(imagens, rotulos)):
        nome_pessoa = nomes[rotulo] if nomes is not None else f"pessoa_{rotulo:03d}"
        nome_pessoa = str(nome_pessoa).replace(" ", "_")
        pasta_pessoa = os.path.join(saida_dir, nome_pessoa)
        os.makedirs(pasta_pessoa, exist_ok=True)

        arr = img
        if arr.max() <= 1.0:
            arr = (arr * 255).astype("uint8")
        else:
            arr = arr.astype("uint8")

        modo = "L" if arr.ndim == 2 else "RGB"
        imagem_pil = Image.fromarray(arr, mode=modo)
        caminho = os.path.join(pasta_pessoa, f"foto_{idx:04d}.jpg")
        imagem_pil.save(caminho, quality=95)


def preparar_lfw(saida_dir: str, min_fotos_por_pessoa: int) -> None:
    from sklearn.datasets import fetch_lfw_people

    print("Baixando LFW (pode levar alguns minutos na primeira vez, ~200MB)...")
    lfw = fetch_lfw_people(min_faces_per_person=min_fotos_por_pessoa, color=True, resize=1.0)
    n_pessoas = len(lfw.target_names)
    print(f"{n_pessoas} pessoas com >= {min_fotos_por_pessoa} fotos cada "
          f"({len(lfw.images)} imagens no total).")
    if n_pessoas < 4:
        print("AVISO: poucas pessoas atendem esse minimo de fotos. "
              "Considere diminuir --min_fotos_por_pessoa (ex.: 10).")
    salvar_pessoas(lfw.images, lfw.target, lfw.target_names, saida_dir)


def preparar_att(saida_dir: str) -> None:
    from sklearn.datasets import fetch_olivetti_faces

    print("Baixando AT&T / Olivetti Faces...")
    att = fetch_olivetti_faces()
    print(f"{len(set(att.target))} pessoas, {len(att.images)} imagens no total.")
    salvar_pessoas(att.images, att.target, None, saida_dir)
    print(
        "\nAVISO: o AT&T/Olivetti e um dataset pequeno, antigo e com condicoes "
        "muito controladas (fundo escuro uniforme, iluminacao de estudio, preto "
        "e branco). Use-o so para validar se o pipeline de benchmark esta "
        "funcionando - NAO como resultado final do TCC, pois nao e representativo "
        "das condicoes reais dentro de um onibus escolar rural."
    )


def main():
    parser = argparse.ArgumentParser(description="Prepara um dataset publico de rostos para o benchmark")
    parser.add_argument("--fonte", choices=["lfw", "att"], default="lfw")
    parser.add_argument(
        "--min_fotos_por_pessoa", type=int, default=15,
        help="So usado com --fonte lfw. Quanto maior, menos pessoas sobram, mas mais robusto o teste.",
    )
    parser.add_argument("--saida", default="./dataset")
    args = parser.parse_args()

    if args.fonte == "lfw":
        preparar_lfw(args.saida, args.min_fotos_por_pessoa)
    else:
        preparar_att(args.saida)

    print(f"\nDataset pronto em: {args.saida}")
    print(f"Agora rode: python benchmark_face_recognition.py --dataset_dir {args.saida}")


if __name__ == "__main__":
    main()
```

### 5.2 `benchmark_face_recognition.py`

Roda os 10 algoritmos (via `DeepFace`) sobre o dataset preparado, calcula acurácia/precisão/recall/F1 e tempo médio de inferência, e gera um CSV + gráfico comparativo.

```python
"""
Benchmark de algoritmos de reconhecimento facial - TCC
Sistema IoT para Monitoramento de Presenca em Transporte Escolar Rural

Compara os principais backbones de reconhecimento facial disponiveis na
biblioteca DeepFace (que ja embala VGG-Face, FaceNet, FaceNet512, OpenFace,
DeepFace, DeepID, ArcFace, Dlib, SFace e GhostFaceNet atras de uma API unica),
em termos de:
    - acuracia (accuracy, precisao, recall, F1)
    - tempo medio de inferencia por par de imagens
    - viabilidade de uso embarcado (Raspberry Pi / acelerador Hailo)

------------------------------------------------------------------------
INSTALACAO (rodar na sua maquina, nao dentro do ambiente do Claude):
    pip install deepface pandas matplotlib opencv-python tf-keras

USO:
    python benchmark_face_recognition.py --dataset_dir ./dataset

ESTRUTURA ESPERADA DO DATASET (uma pasta por pessoa):
    dataset/
        pessoa_01/
            foto1.jpg
            foto2.jpg
            foto3.jpg
        pessoa_02/
            foto1.jpg
            foto2.jpg
        ...

    Use no minimo 2 fotos por pessoa e pelo menos 4-5 pessoas diferentes
    para o benchmark fazer sentido estatisticamente.

    IMPORTANTE (privacidade / LGPD): nesta fase de prototipagem, NAO use
    fotos reais de alunos menores de idade. Use fotos da equipe do projeto
    ou um subconjunto publico como o LFW (http://vis-www.cs.umass.edu/lfw/).

SAIDA:
    - benchmark_resultados.csv      -> tabela com metricas de cada modelo
    - benchmark_resultados.png      -> grafico acuracia x tempo de inferencia
    - impressao no terminal de um ranking ordenado por acuracia
------------------------------------------------------------------------
"""

import argparse
import itertools
import os
import random
import time
from dataclasses import dataclass, field

import pandas as pd

# Os 10 algoritmos analisados na revisao bibliografica (Atividade 1.2).
# Todos sao acessiveis atraves da mesma API do DeepFace, o que permite um
# benchmark justo (mesmo pipeline de deteccao/alinhamento para todos).
MODELOS = [
    "VGG-Face",
    "Facenet",
    "Facenet512",
    "OpenFace",
    "DeepFace",
    "DeepID",
    "ArcFace",
    "Dlib",
    "SFace",
    "GhostFaceNet",
]

# Tamanhos aproximados de cada modelo em disco (MB), conforme documentacao
# do DeepFace/artigos originais. Usados so para contextualizar o quao
# "embarcavel" cada opcao e - nao sao medidos automaticamente pelo script.
TAMANHO_APROX_MB = {
    "VGG-Face": 580,
    "Facenet": 90,
    "Facenet512": 90,
    "OpenFace": 30,
    "DeepFace": 150,
    "DeepID": 3,
    "ArcFace": 130,
    "Dlib": 22,
    "SFace": 5,
    "GhostFaceNet": 16,
}

# Detector leve, mais proximo do que roda bem em Raspberry Pi / Hailo.
# Pode trocar por "retinaface" ou "mtcnn" se quiser mais precisao (e mais
# custo computacional) na deteccao/alinhamento do rosto.
DETECTOR_PADRAO = "opencv"


@dataclass
class ParImagem:
    img1: str
    img2: str
    mesma_pessoa: bool


def montar_pares(dataset_dir: str, pares_por_pessoa: int, seed: int = 42) -> list:
    """Monta pares positivos (mesma pessoa) e negativos (pessoas diferentes)
    a partir da estrutura de pastas do dataset."""
    random.seed(seed)
    pessoas = {
        nome: [
            os.path.join(dataset_dir, nome, arq)
            for arq in sorted(os.listdir(os.path.join(dataset_dir, nome)))
            if arq.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
        for nome in sorted(os.listdir(dataset_dir))
        if os.path.isdir(os.path.join(dataset_dir, nome))
    }
    pessoas = {nome: fotos for nome, fotos in pessoas.items() if len(fotos) >= 2}

    if len(pessoas) < 2:
        raise ValueError(
            "Dataset precisa de pelo menos 2 pessoas, cada uma com 2+ fotos. "
            f"Encontrado: {len(pessoas)} pessoa(s) valida(s) em '{dataset_dir}'."
        )

    pares: list[ParImagem] = []

    # Pares positivos: combinacoes de fotos da mesma pessoa
    for nome, fotos in pessoas.items():
        combinacoes = list(itertools.combinations(fotos, 2))
        random.shuffle(combinacoes)
        for img1, img2 in combinacoes[:pares_por_pessoa]:
            pares.append(ParImagem(img1, img2, mesma_pessoa=True))

    # Pares negativos: mesma quantidade, pessoas diferentes sorteadas
    nomes = list(pessoas.keys())
    n_negativos = len(pares)
    tentativas = 0
    while len([p for p in pares if not p.mesma_pessoa]) < n_negativos and tentativas < n_negativos * 20:
        tentativas += 1
        nome1, nome2 = random.sample(nomes, 2)
        img1 = random.choice(pessoas[nome1])
        img2 = random.choice(pessoas[nome2])
        pares.append(ParImagem(img1, img2, mesma_pessoa=False))

    random.shuffle(pares)
    return pares


def avaliar_modelo(modelo: str, pares: list, detector_backend: str) -> dict:
    """Roda DeepFace.verify para um modelo em todos os pares e calcula metricas."""
    from deepface import DeepFace  # import tardio: so precisa quando for usar

    vp = vn = fp = fn = 0  # verdadeiro/falso positivo/negativo
    tempos = []
    erros = 0

    for par in pares:
        inicio = time.perf_counter()
        try:
            resultado = DeepFace.verify(
                img1_path=par.img1,
                img2_path=par.img2,
                model_name=modelo,
                detector_backend=detector_backend,
                enforce_detection=False,  # nao falha se a deteccao for imperfeita
            )
            previsto_mesma_pessoa = bool(resultado["verified"])
        except Exception:
            erros += 1
            continue
        tempos.append(time.perf_counter() - inicio)

        if par.mesma_pessoa and previsto_mesma_pessoa:
            vp += 1
        elif par.mesma_pessoa and not previsto_mesma_pessoa:
            fn += 1
        elif not par.mesma_pessoa and previsto_mesma_pessoa:
            fp += 1
        else:
            vn += 1

    total = vp + vn + fp + fn
    if total == 0:
        return {
            "modelo": modelo, "acuracia": None, "precisao": None, "recall": None,
            "f1": None, "tempo_medio_s": None, "pares_avaliados": 0, "erros": erros,
            "tamanho_aprox_mb": TAMANHO_APROX_MB.get(modelo),
        }

    acuracia = (vp + vn) / total
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0.0
    f1 = (2 * precisao * recall / (precisao + recall)) if (precisao + recall) > 0 else 0.0
    tempo_medio = sum(tempos) / len(tempos) if tempos else None

    return {
        "modelo": modelo,
        "acuracia": round(acuracia, 4),
        "precisao": round(precisao, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "tempo_medio_s": round(tempo_medio, 4) if tempo_medio else None,
        "pares_avaliados": total,
        "erros": erros,
        "tamanho_aprox_mb": TAMANHO_APROX_MB.get(modelo),
    }


def gerar_grafico(df: pd.DataFrame, caminho_saida: str) -> None:
    import matplotlib.pyplot as plt

    df_validos = df.dropna(subset=["acuracia", "tempo_medio_s"])
    if df_validos.empty:
        print("Nenhum resultado valido para plotar.")
        return

    fig, ax1 = plt.subplots(figsize=(10, 6))
    x = range(len(df_validos))
    ax1.bar(x, df_validos["acuracia"], color="steelblue", label="Acuracia")
    ax1.set_ylabel("Acuracia")
    ax1.set_ylim(0, 1)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(df_validos["modelo"], rotation=45, ha="right")

    ax2 = ax1.twinx()
    ax2.plot(x, df_validos["tempo_medio_s"], color="firebrick", marker="o", label="Tempo medio (s)")
    ax2.set_ylabel("Tempo medio por par (s)")

    fig.suptitle("Comparacao de algoritmos de reconhecimento facial")
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=150)
    print(f"Grafico salvo em: {caminho_saida}")


def main():
    parser = argparse.ArgumentParser(description="Benchmark de reconhecimento facial")
    parser.add_argument("--dataset_dir", required=True, help="Pasta com uma subpasta por pessoa")
    parser.add_argument("--pares_por_pessoa", type=int, default=3, help="Nº de pares positivos por pessoa")
    parser.add_argument("--detector_backend", default=DETECTOR_PADRAO, help="opencv, retinaface, mtcnn, yunet...")
    parser.add_argument(
        "--modelos", nargs="*", default=MODELOS,
        help="Subconjunto de modelos a testar (default: todos os 10)",
    )
    parser.add_argument("--saida_csv", default="benchmark_resultados.csv")
    parser.add_argument("--saida_png", default="benchmark_resultados.png")
    args = parser.parse_args()

    pares = montar_pares(args.dataset_dir, args.pares_por_pessoa)
    print(f"{len(pares)} pares montados "
          f"({sum(p.mesma_pessoa for p in pares)} positivos, "
          f"{sum(not p.mesma_pessoa for p in pares)} negativos).")

    resultados = []
    for modelo in args.modelos:
        print(f"\n== Avaliando {modelo} ==")
        resultado = avaliar_modelo(modelo, pares, args.detector_backend)
        print(resultado)
        resultados.append(resultado)

    df = pd.DataFrame(resultados).sort_values("acuracia", ascending=False)
    df.to_csv(args.saida_csv, index=False)
    print(f"\nResultados salvos em: {args.saida_csv}")
    print("\nRanking (melhor -> pior acuracia):")
    print(df.to_string(index=False))

    gerar_grafico(df, args.saida_png)

    print("\nSugestao: cruze este ranking com a coluna 'tamanho_aprox_mb' e o "
          "tempo_medio_s para escolher os 2 modelos que melhor equilibram "
          "acuracia e viabilidade de embarque (Raspberry Pi / Hailo).")


if __name__ == "__main__":
    main()
```

---

## 6. Fluxo de uso completo (rodar na sua máquina)

```bash
pip install scikit-learn pillow deepface pandas matplotlib opencv-python tf-keras

# 1) baixa e organiza o dataset
python preparar_dataset.py --fonte lfw --min_fotos_por_pessoa 15 --saida ./dataset

# 2) roda o benchmark dos 10 algoritmos
python benchmark_face_recognition.py --dataset_dir ./dataset
```

---

## 7. Próximos passos sugeridos

- Rodar o benchmark e interpretar os resultados junto com a orientação.
- Testar a etapa de **detecção** separadamente (YuNet vs RetinaFace vs MTCNN), já que a acurácia final depende dos dois estágios (detecção + reconhecimento).
- Escrever a seção de Revisão Bibliográfica (Atividade 1.2) da monografia com base nessa comparação, citando as fontes corretamente.
- Se o LFW se mostrar pequeno demais, considerar VGGFace2 ou "Pins Face Recognition" (Kaggle) para mais volume/diversidade.
