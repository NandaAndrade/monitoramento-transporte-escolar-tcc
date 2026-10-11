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
INSTALACAO:
    pip install -e ".[pesquisa]"

    O extra "pesquisa" fixa opencv-python em 4.10.0.84: a 5.0.0 (mais recente
    do PyPI) nao inclui os arquivos de cascata Haar e quebra o detector
    "opencv" silenciosamente (todos os pares dao erro sem mensagem clara).

    Dois dos 10 modelos exigem setup extra, alem do pip install acima:

    - Dlib: nao ha wheel pre-compilada para Python 3.13 no Windows. E preciso
      compilar do codigo-fonte (`pip install dlib` vai tentar compilar na
      hora) - isso exige CMake (`pip install cmake`) e um compilador C++
      (ex.: Visual Studio Build Tools com o workload de MSVC). Sem isso, a
      instalacao do dlib falha antes mesmo de rodar o script.
    - DeepFace (o modelo "Facebook DeepFace" de 2014, nao confundir com a
      biblioteca DeepFace): usa uma camada Keras (`LocallyConnected2D`)
      removida do TensorFlow apos a versao 2.12, incompativel com o
      TensorFlow exigido por Python 3.13. Para rodar esse modelo especifico,
      e necessario um segundo ambiente virtual com Python 3.10 (ou outra
      versao compativel com TF <=2.12) e `tensorflow<=2.12` instalado -
      isolado do ambiente principal, para nao rebaixar o TF usado pelos
      outros 9 modelos. Rode o script dentro desse segundo ambiente so para
      avaliar o modelo "DeepFace" (--modelos DeepFace).

    Mais detalhes de como isso foi resolvido neste projeto (build do Dlib
    com CMake/MSVC, criacao do venv legado) estao em
    docs/benchmark_reconhecimento_facial.md, secao 3.

USO (a partir da raiz do repositorio):
    python pesquisa/benchmark_reconhecimento_facial.py --pares_por_pessoa 2

    Sem --dataset_dir, usa o LFW em pesquisa/dados/lfw/. Com --pares_por_pessoa 2
    reproduz os 384 pares dos resultados publicados.

    Com detectores pesados (retinaface, mtcnn), use o cache de deteccao: cada
    imagem e detectada uma unica vez e os modelos rodam sobre os recortes.
    python pesquisa/benchmark_reconhecimento_facial.py --pares_por_pessoa 2 \\
        --detector_backend retinaface --cache_deteccao \\
        --saida_csv pesquisa/resultados/benchmark_resultados_retinaface.csv \\
        --saida_png pesquisa/resultados/benchmark_resultados_retinaface.png

ESTRUTURA ESPERADA DO DATASET (uma pasta por pessoa):
    pesquisa/dados/lfw/
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

SAIDA (em pesquisa/resultados/):
    - benchmark_resultados.csv      -> tabela com metricas de cada modelo
    - benchmark_resultados.png      -> grafico acuracia x tempo de inferencia
    - impressao no terminal de um ranking ordenado por acuracia
------------------------------------------------------------------------
"""

import argparse
import itertools
import logging
import multiprocessing as mp
import random
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

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

EXTENSOES_IMAGEM = (".jpg", ".jpeg", ".png")

# Caminhos relativos a pasta pesquisa/, para o script funcionar de qualquer diretorio.
PASTA_PESQUISA = Path(__file__).resolve().parent
DATASET_PADRAO = PASTA_PESQUISA / "dados" / "lfw"
PASTA_RESULTADOS = PASTA_PESQUISA / "resultados"
PASTA_CACHE_DETECCAO = PASTA_PESQUISA / "cache_deteccao"

# Limite de sorteios para os pares negativos, para nao entrar em laco infinito.
TENTATIVAS_POR_NEGATIVO = 20

# A cada quantos pares/imagens o progresso aparece no log.
INTERVALO_PROGRESSO = 50

# Detector usado quando o rosto ja vem recortado do cache.
DETECTOR_SEM_DETECCAO = "skip"


@dataclass(frozen=True)
class ParImagem:
    img1: str
    img2: str
    mesma_pessoa: bool


@dataclass
class MatrizConfusao:
    vp: int = 0  # verdadeiro positivo
    vn: int = 0  # verdadeiro negativo
    fp: int = 0  # falso positivo
    fn: int = 0  # falso negativo

    @property
    def total(self) -> int:
        return self.vp + self.vn + self.fp + self.fn

    def registrar(self, esperado_mesma_pessoa: bool, previsto_mesma_pessoa: bool) -> None:
        if esperado_mesma_pessoa and previsto_mesma_pessoa:
            self.vp += 1
        elif esperado_mesma_pessoa:
            self.fn += 1
        elif previsto_mesma_pessoa:
            self.fp += 1
        else:
            self.vn += 1


@dataclass(frozen=True)
class ResultadoModelo:
    """Uma linha do CSV de resultados."""

    modelo: str
    acuracia: float | None
    precisao: float | None
    recall: float | None
    f1: float | None
    tempo_medio_s: float | None
    pares_avaliados: int
    erros: int
    tamanho_aprox_mb: int | None
    detector: str | None = None
    # Tempo medio de deteccao por imagem; so e medido com --cache_deteccao.
    tempo_deteccao_s: float | None = None


def listar_fotos_por_pessoa(dataset_dir: str | Path) -> dict[str, list[str]]:
    """Le o dataset (uma pasta por pessoa) e mantem so quem tem 2+ fotos."""
    raiz = Path(dataset_dir)
    pessoas = {
        pasta.name: [
            str(arquivo)
            for arquivo in sorted(pasta.iterdir())
            if arquivo.name.lower().endswith(EXTENSOES_IMAGEM)
        ]
        for pasta in sorted(raiz.iterdir())
        if pasta.is_dir()
    }
    return {nome: fotos for nome, fotos in pessoas.items() if len(fotos) >= 2}


def montar_pares(dataset_dir: str | Path, pares_por_pessoa: int, seed: int = 42) -> list[ParImagem]:
    """Monta pares positivos (mesma pessoa) e negativos (pessoas diferentes).

    A ordem das chamadas a `random` e mantida igual a da versao original do
    script, para que a mesma semente gere exatamente os mesmos pares.
    """
    random.seed(seed)
    pessoas = listar_fotos_por_pessoa(dataset_dir)
    if len(pessoas) < 2:
        raise ValueError(
            "Dataset precisa de pelo menos 2 pessoas, cada uma com 2+ fotos. "
            f"Encontrado: {len(pessoas)} pessoa(s) valida(s) em '{dataset_dir}'."
        )

    pares = _pares_positivos(pessoas, pares_por_pessoa)
    pares += _pares_negativos(pessoas, quantidade=len(pares))
    random.shuffle(pares)
    return pares


def _pares_positivos(pessoas: dict[str, list[str]], pares_por_pessoa: int) -> list[ParImagem]:
    pares = []
    for fotos in pessoas.values():
        combinacoes = list(itertools.combinations(fotos, 2))
        random.shuffle(combinacoes)
        for img1, img2 in combinacoes[:pares_por_pessoa]:
            pares.append(ParImagem(img1, img2, mesma_pessoa=True))
    return pares


def _pares_negativos(pessoas: dict[str, list[str]], quantidade: int) -> list[ParImagem]:
    nomes = list(pessoas.keys())
    pares = []
    tentativas = 0
    while len(pares) < quantidade and tentativas < quantidade * TENTATIVAS_POR_NEGATIVO:
        tentativas += 1
        nome1, nome2 = random.sample(nomes, 2)
        img1 = random.choice(pessoas[nome1])
        img2 = random.choice(pessoas[nome2])
        pares.append(ParImagem(img1, img2, mesma_pessoa=False))
    return pares


def calcular_resultado(
    modelo: str, matriz: MatrizConfusao, tempos: list[float], erros: int
) -> ResultadoModelo:
    """Calcula acuracia, precisao, recall, F1 e tempo medio a partir da matriz de confusao."""
    tamanho = TAMANHO_APROX_MB.get(modelo)
    if matriz.total == 0:
        return ResultadoModelo(modelo, None, None, None, None, None, 0, erros, tamanho)

    vp, vn, fp, fn = matriz.vp, matriz.vn, matriz.fp, matriz.fn
    acuracia = (vp + vn) / matriz.total
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0.0
    f1 = (2 * precisao * recall / (precisao + recall)) if (precisao + recall) > 0 else 0.0
    tempo_medio = sum(tempos) / len(tempos) if tempos else None

    return ResultadoModelo(
        modelo=modelo,
        acuracia=round(acuracia, 4),
        precisao=round(precisao, 4),
        recall=round(recall, 4),
        f1=round(f1, 4),
        tempo_medio_s=round(tempo_medio, 4) if tempo_medio else None,
        pares_avaliados=matriz.total,
        erros=erros,
        tamanho_aprox_mb=tamanho,
    )


def caminho_no_cache(imagem: str, cache_dir: str | Path) -> Path:
    """Recorte de `<dataset>/<pessoa>/<foto>` fica em `<cache_dir>/<pessoa>/<foto>`."""
    origem = Path(imagem)
    return Path(cache_dir) / origem.parent.name / origem.name


def _desligar_ampliacao_retinaface() -> None:
    """Impede a lib retinaface de ampliar cada imagem ate o menor lado ter 1024 px.

    O DeepFace nao expoe o parametro `allow_upscaling`. Com as fotos de 125x94
    do LFW a ampliacao faz cada deteccao levar ~17 s em CPU; sem ela cai para
    ~0,6 s e o rosto continua sendo encontrado (testado em 40 imagens: 40/40).
    """
    from retinaface import RetinaFace

    detectar_original = RetinaFace.detect_faces

    def detectar_sem_ampliar(*args, **kwargs):
        return detectar_original(*args, **{**kwargs, "allow_upscaling": False})

    RetinaFace.detect_faces = detectar_sem_ampliar


def preparar_cache_deteccao(
    pares: list[ParImagem], detector_backend: str, cache_dir: str | Path
) -> tuple[list[ParImagem], float | None]:
    """Detecta o rosto UMA vez por imagem e devolve os pares apontando para os recortes.

    Sem isso, DeepFace.verify roda a deteccao de novo nas duas imagens de cada
    par, para cada modelo. Com o Haar Cascade (opencv) isso e barato, mas com
    detectores pesados como o RetinaFace em CPU a rodada nao termina nem o
    primeiro modelo em 2 h. Com o cache, os modelos rodam com detector "skip"
    sobre os recortes, e o tempo de deteccao e medido a parte.

    Se a imagem tiver mais de um rosto, fica o de maior area: no LFW o rosto da
    pessoa rotulada e o central e, em geral, o maior da foto. Recortes ja
    existentes no cache sao reaproveitados, o que permite retomar a rodada.
    Tambem devolve o tempo medio de deteccao por imagem (None se tudo veio do cache).
    """
    import cv2
    import numpy as np
    from deepface import DeepFace

    imagens = sorted({p.img1 for p in pares} | {p.img2 for p in pares})
    faltando = [img for img in imagens if not caminho_no_cache(img, cache_dir).exists()]
    if detector_backend == "retinaface" and faltando:
        _desligar_ampliacao_retinaface()

    tempos = []
    for i, imagem in enumerate(faltando, start=1):
        destino = caminho_no_cache(imagem, cache_dir)
        destino.parent.mkdir(parents=True, exist_ok=True)
        inicio = time.perf_counter()
        rostos = DeepFace.extract_faces(
            img_path=imagem,
            detector_backend=detector_backend,
            enforce_detection=False,  # igual ao verify: sem rosto, usa a imagem inteira
            align=True,
            color_face="bgr",
            normalize_face=False,
        )
        tempos.append(time.perf_counter() - inicio)
        maior = max(rostos, key=lambda r: r["facial_area"]["w"] * r["facial_area"]["h"])
        cv2.imwrite(str(destino), np.clip(maior["face"], 0, 255).astype("uint8"))
        if i % INTERVALO_PROGRESSO == 0 or i == len(faltando):
            logger.info("  deteccao: %d/%d imagens", i, len(faltando))

    novos_pares = [
        ParImagem(
            str(caminho_no_cache(p.img1, cache_dir)),
            str(caminho_no_cache(p.img2, cache_dir)),
            p.mesma_pessoa,
        )
        for p in pares
    ]
    tempo_medio = sum(tempos) / len(tempos) if tempos else None
    return novos_pares, tempo_medio


def avaliar_modelo(modelo: str, pares: list[ParImagem], detector_backend: str) -> ResultadoModelo:
    """Roda DeepFace.verify para um modelo em todos os pares e calcula metricas."""
    from deepface import DeepFace  # import tardio: so precisa quando for usar

    matriz = MatrizConfusao()
    tempos = []
    erros = 0

    for i, par in enumerate(pares, start=1):
        if i % INTERVALO_PROGRESSO == 0:
            logger.info("  %s: %d/%d pares", modelo, i, len(pares))
        inicio = time.perf_counter()
        try:
            resultado = DeepFace.verify(
                img1_path=par.img1,
                img2_path=par.img2,
                model_name=modelo,
                detector_backend=detector_backend,
                enforce_detection=False,  # nao falha se a deteccao for imperfeita
            )
        except Exception as erro:  # o DeepFace nao tem uma hierarquia de excecoes propria
            logger.warning("%s falhou em (%s, %s): %s", modelo, par.img1, par.img2, erro)
            erros += 1
            continue
        tempos.append(time.perf_counter() - inicio)
        matriz.registrar(par.mesma_pessoa, bool(resultado["verified"]))

    return calcular_resultado(modelo, matriz, tempos, erros)


def _avaliar_modelo_worker(
    modelo: str, pares: list[ParImagem], detector_backend: str, fila: mp.Queue
) -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # Devolve um dict: a classe criada no processo filho nao e reconstruida no pai.
    fila.put(asdict(avaliar_modelo(modelo, pares, detector_backend)))


def avaliar_modelo_isolado(
    modelo: str, pares: list[ParImagem], detector_backend: str
) -> ResultadoModelo:
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
    fila: mp.Queue = ctx.Queue()
    processo = ctx.Process(
        target=_avaliar_modelo_worker, args=(modelo, pares, detector_backend, fila)
    )
    processo.start()
    resultado = ResultadoModelo(**fila.get())
    processo.join()
    return resultado


def gerar_grafico(df: "pd.DataFrame", caminho_saida: str) -> None:
    import matplotlib.pyplot as plt

    df_validos = df.dropna(subset=["acuracia", "tempo_medio_s"])
    if df_validos.empty:
        logger.warning("Nenhum resultado valido para plotar.")
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
    logger.info("Grafico salvo em: %s", caminho_saida)


def _argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark de reconhecimento facial")
    parser.add_argument(
        "--dataset_dir", default=str(DATASET_PADRAO), help="Pasta com uma subpasta por pessoa"
    )
    parser.add_argument(
        "--pares_por_pessoa", type=int, default=3, help="Nº de pares positivos por pessoa"
    )
    parser.add_argument(
        "--detector_backend", default=DETECTOR_PADRAO, help="opencv, retinaface, mtcnn, yunet..."
    )
    parser.add_argument(
        "--modelos",
        nargs="*",
        default=MODELOS,
        help="Subconjunto de modelos a testar (default: todos os 10)",
    )
    parser.add_argument(
        "--cache_deteccao",
        nargs="?",
        const="",
        default=None,
        help="Detecta os rostos uma unica vez por imagem e salva os recortes; os modelos "
        "passam a rodar com detector 'skip' sobre eles. Recomendado para detectores "
        "pesados (retinaface, mtcnn). Sem valor, usa pesquisa/cache_deteccao/<detector>/.",
    )
    parser.add_argument("--saida_csv", default=str(PASTA_RESULTADOS / "benchmark_resultados.csv"))
    parser.add_argument("--saida_png", default=str(PASTA_RESULTADOS / "benchmark_resultados.png"))
    parser.add_argument(
        "--sem_isolamento",
        action="store_true",
        help="Roda todos os modelos no mesmo processo (mais rapido de configurar, mas o "
        "tempo_medio_s de modelos avaliados por ultimo fica distorcido por causa dos "
        "modelos anteriores ainda residentes em memoria). Por padrao cada modelo roda "
        "isolado em um processo novo para medir tempo de inferencia de forma justa.",
    )
    return parser.parse_args()


def main() -> None:
    import pandas as pd

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    args = _argumentos()

    pares = montar_pares(args.dataset_dir, args.pares_por_pessoa)
    positivos = sum(p.mesma_pessoa for p in pares)
    logger.info(
        "%d pares montados (%d positivos, %d negativos).",
        len(pares),
        positivos,
        len(pares) - positivos,
    )

    detector = args.detector_backend
    tempo_deteccao = None
    if args.cache_deteccao is not None and detector != DETECTOR_SEM_DETECCAO:
        cache_dir = args.cache_deteccao or PASTA_CACHE_DETECCAO / detector
        logger.info("\n== Detectando rostos com %s (uma vez por imagem) ==", detector)
        pares, tempo_deteccao = preparar_cache_deteccao(pares, detector, cache_dir)
        detector = DETECTOR_SEM_DETECCAO

    avaliar = avaliar_modelo if args.sem_isolamento else avaliar_modelo_isolado
    resultados = []
    for modelo in args.modelos:
        logger.info("\n== Avaliando %s ==", modelo)
        resultado = replace(
            avaliar(modelo, pares, detector),
            detector=args.detector_backend,
            tempo_deteccao_s=round(tempo_deteccao, 4) if tempo_deteccao else None,
        )
        logger.info("%s", resultado)
        resultados.append(asdict(resultado))
        # Salva a cada modelo, para nao perder tudo se a rodada for interrompida.
        pd.DataFrame(resultados).to_csv(args.saida_csv, index=False)

    df = pd.DataFrame(resultados).sort_values("acuracia", ascending=False)
    df.to_csv(args.saida_csv, index=False)
    logger.info("\nResultados salvos em: %s", args.saida_csv)
    logger.info("\nRanking (melhor -> pior acuracia):\n%s", df.to_string(index=False))

    gerar_grafico(df, args.saida_png)

    logger.info(
        "\nSugestao: cruze este ranking com a coluna 'tamanho_aprox_mb' e o "
        "tempo_medio_s para escolher os 2 modelos que melhor equilibram "
        "acuracia e viabilidade de embarque (Raspberry Pi / Hailo)."
    )


if __name__ == "__main__":
    main()
