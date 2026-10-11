"""
Comparacao de detectores de rosto (OpenCV x RetinaFace) no benchmark - TCC

Junta as rodadas feitas com --cache_deteccao (mesma metodologia para os dois
detectores: deteccao uma vez por imagem, mesmos 384 pares do LFW, tempo de
deteccao medido a parte) e gera, em pesquisa/resultados/:
    - benchmark_comparacao_detectores.csv -> uma linha por modelo, com
      acuracia, recall e tempos (deteccao, reconhecimento, total) por detector
    - benchmark_comparacao_detectores.png -> acuracia e tempo total por par

O modelo DeepFace (Facebook) roda em outro ambiente (.venv_deepface_legacy,
TensorFlow <= 2.12), entao sai num CSV separado (*_deepface.csv); aqui ele e
incorporado ao CSV principal de cada detector, e o CSV separado e apagado.
Como essas rodadas reaproveitam o cache, o tempo de deteccao delas vem vazio e
e preenchido com o da rodada principal.

------------------------------------------------------------------------
INSTALACAO:
    pip install -e ".[pesquisa]"

USO (a partir da raiz do repositorio, depois das rodadas com cada detector):
    python pesquisa/comparar_detectores.py
------------------------------------------------------------------------
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

logger = logging.getLogger(__name__)

PASTA_RESULTADOS = Path(__file__).resolve().parent / "resultados"

# Para cada detector: (CSV principal, CSV do modelo DeepFace rodado no ambiente legado).
DETECTORES = {
    "opencv": (
        "benchmark_resultados_opencv_cache.csv",
        "benchmark_resultados_opencv_cache_deepface.csv",
    ),
    "retinaface": (
        "benchmark_resultados_retinaface.csv",
        "benchmark_resultados_retinaface_deepface.csv",
    ),
}
SAIDA_CSV = PASTA_RESULTADOS / "benchmark_comparacao_detectores.csv"
SAIDA_PNG = PASTA_RESULTADOS / "benchmark_comparacao_detectores.png"

# Metas do levantamento de requisitos (docs/requisitos.md)
META_ACURACIA = 0.90  # RNF-03
LIMITE_TEMPO_S = 2.0  # RNF-02

# O verify detecta as duas imagens do par.
IMAGENS_POR_PAR = 2

COR = {"opencv": "#2a78d6", "retinaface": "#eb6834"}
MARCADOR = {"opencv": "o", "retinaface": "s"}
ROTULO = {"opencv": "OpenCV (Haar Cascade)", "retinaface": "RetinaFace"}
COR_TEXTO, COR_TEXTO_SECUNDARIO, COR_GRADE = "#0b0b0b", "#52514e", "#e4e3df"
MARCAS_TEMPO_S = [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20]


def carregar(detector: str) -> "pd.DataFrame":
    """Le o CSV de um detector, incorporando o CSV do DeepFace legado se ele existir."""
    import pandas as pd

    principal, legado = (PASTA_RESULTADOS / nome for nome in DETECTORES[detector])
    df = pd.read_csv(principal)
    if legado.exists():
        df = pd.concat([df[df["modelo"] != "DeepFace"], pd.read_csv(legado)], ignore_index=True)
        df["tempo_deteccao_s"] = df["tempo_deteccao_s"].ffill().bfill()
        df = df.sort_values("acuracia", ascending=False)
        df.to_csv(principal, index=False)  # o CSV principal passa a ter os 10 modelos
        legado.unlink()
        logger.info("%s incorporado a %s", legado.name, principal.name)
    df["tempo_total_par_s"] = (
        df["tempo_medio_s"] + IMAGENS_POR_PAR * df["tempo_deteccao_s"]
    ).round(4)
    return df


def montar_comparacao() -> "pd.DataFrame":
    """Uma linha por modelo, com as metricas de cada detector lado a lado."""
    import pandas as pd

    colunas = ["acuracia", "recall", "tempo_deteccao_s", "tempo_medio_s", "tempo_total_par_s"]
    partes = []
    for detector in DETECTORES:
        df = carregar(detector).set_index("modelo")[colunas]
        partes.append(
            df.rename(
                columns={
                    "acuracia": f"acuracia_{detector}",
                    "recall": f"recall_{detector}",
                    "tempo_deteccao_s": f"tempo_deteccao_img_{detector}",
                    "tempo_medio_s": f"tempo_reconhecimento_par_{detector}",
                    "tempo_total_par_s": f"tempo_total_par_{detector}",
                }
            )
        )
    comparacao = pd.concat(partes, axis=1).reset_index()
    return comparacao.sort_values("acuracia_retinaface", ascending=False)


def _estilizar_eixo(ax, titulo_x: str) -> None:
    ax.set_xlabel(titulo_x, color=COR_TEXTO_SECUNDARIO)
    ax.grid(axis="x", color=COR_GRADE, linewidth=0.8)
    ax.set_axisbelow(True)
    for lado in ("top", "right", "left"):
        ax.spines[lado].set_visible(False)
    ax.spines["bottom"].set_color(COR_GRADE)
    ax.tick_params(colors=COR_TEXTO_SECUNDARIO, length=0)


def gerar_grafico(comparacao: "pd.DataFrame", caminho: Path) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FuncFormatter

    comparacao = comparacao.sort_values("acuracia_retinaface")
    y = range(len(comparacao))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5.5), sharey=True, facecolor="white")
    paineis = [
        (ax1, "acuracia", 100, "Acurácia (%)", META_ACURACIA * 100, "meta RNF-03 (90%)"),
        (
            ax2,
            "tempo_total_par",
            1,
            "Tempo total por par (s, escala log)",
            LIMITE_TEMPO_S,
            "limite RNF-02 (2 s)",
        ),
    ]
    for ax, campo, escala, titulo_x, referencia, rotulo_referencia in paineis:
        a = comparacao[f"{campo}_opencv"] * escala
        b = comparacao[f"{campo}_retinaface"] * escala
        ax.hlines(y, a.clip(upper=b), a.clip(lower=b), color=COR_GRADE, linewidth=2, zorder=1)
        # Quadrado maior por baixo e circulo menor por cima: quando os valores
        # coincidem, os dois continuam visiveis.
        for detector, valores, tamanho, z in (("opencv", a, 50, 4), ("retinaface", b, 110, 3)):
            ax.scatter(
                valores,
                y,
                s=tamanho,
                marker=MARCADOR[detector],
                color=COR[detector],
                edgecolor="white",
                linewidth=1.5,
                zorder=z,
                label=ROTULO[detector],
            )
        ax.axvline(referencia, color=COR_TEXTO_SECUNDARIO, linestyle="--", linewidth=1, zorder=0)
        ax.text(
            referencia,
            len(comparacao) - 0.4,
            rotulo_referencia,
            color=COR_TEXTO_SECUNDARIO,
            fontsize=8,
            ha="center",
            va="bottom",
        )
        _estilizar_eixo(ax, titulo_x)

    ax2.set_xscale("log")
    ax2.xaxis.set_major_locator(FixedLocator(MARCAS_TEMPO_S))
    ax2.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}".replace(".", ",")))
    ax2.xaxis.set_minor_locator(FixedLocator([]))
    ax1.set_yticks(list(y))
    ax1.set_yticklabels(comparacao["modelo"], color=COR_TEXTO)

    ax1.legend(loc="lower right", frameon=False, fontsize=9, labelcolor=COR_TEXTO)
    fig.suptitle(
        "Efeito do detector de rosto no benchmark (384 pares, LFW)",
        color=COR_TEXTO,
        x=0.02,
        ha="left",
    )
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    logger.info("Grafico salvo em: %s", caminho)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    comparacao = montar_comparacao()
    comparacao.to_csv(SAIDA_CSV, index=False)
    logger.info("%s", comparacao.to_string(index=False))
    gerar_grafico(comparacao, SAIDA_PNG)


if __name__ == "__main__":
    main()
