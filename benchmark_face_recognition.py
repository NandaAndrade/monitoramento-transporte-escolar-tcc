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
import multiprocessing as mp
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


def _avaliar_modelo_worker(modelo: str, pares: list, detector_backend: str, queue: "mp.Queue") -> None:
    queue.put(avaliar_modelo(modelo, pares, detector_backend))


def avaliar_modelo_isolado(modelo: str, pares: list, detector_backend: str) -> dict:
    """Roda avaliar_modelo em um processo separado.

    O DeepFace mantem em cache (na memoria do processo) todo modelo ja
    carregado e nunca libera. Rodando varios modelos TensorFlow pesados
    (VGG-Face, Facenet, ArcFace...) no mesmo processo, os modelos avaliados
    por ultimo competem por CPU com os anteriores ainda residentes na
    memoria - observado na pratica: SFace isolado leva ~0.09s/par, mas
    ~4.2s/par quando roda depois de 6 outros modelos carregados no mesmo
    processo. Isolar cada modelo em um processo novo evita essa distorcao
    e da um tempo de inferencia mais realista para a comparacao.
    """
    ctx = mp.get_context("spawn")
    queue: "mp.Queue" = ctx.Queue()
    processo = ctx.Process(target=_avaliar_modelo_worker, args=(modelo, pares, detector_backend, queue))
    processo.start()
    resultado = queue.get()
    processo.join()
    return resultado


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
    parser.add_argument(
        "--sem_isolamento", action="store_true",
        help="Roda todos os modelos no mesmo processo (mais rapido de configurar, mas o "
             "tempo_medio_s de modelos avaliados por ultimo fica distorcido por causa dos "
             "modelos anteriores ainda residentes em memoria). Por padrao cada modelo roda "
             "isolado em um processo novo para medir tempo de inferencia de forma justa.",
    )
    args = parser.parse_args()

    pares = montar_pares(args.dataset_dir, args.pares_por_pessoa)
    print(f"{len(pares)} pares montados "
          f"({sum(p.mesma_pessoa for p in pares)} positivos, "
          f"{sum(not p.mesma_pessoa for p in pares)} negativos).")

    resultados = []
    for modelo in args.modelos:
        print(f"\n== Avaliando {modelo} ==")
        if args.sem_isolamento:
            resultado = avaliar_modelo(modelo, pares, args.detector_backend)
        else:
            resultado = avaliar_modelo_isolado(modelo, pares, args.detector_backend)
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
