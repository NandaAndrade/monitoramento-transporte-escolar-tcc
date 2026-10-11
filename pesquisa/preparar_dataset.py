"""
pesquisa/preparar_dataset.py - TCC: reconhecimento facial para presenca em transporte escolar

Baixa um dataset PUBLICO de rostos (via scikit-learn, sem precisar de link
manual) e organiza as imagens na estrutura de pastas esperada pelo
pesquisa/benchmark_reconhecimento_facial.py:

    pesquisa/dados/lfw/
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
INSTALACAO:
    pip install -e ".[pesquisa]"

USO (a partir da raiz do repositorio):
    # Dataset "de verdade", citavel na monografia -> pesquisa/dados/lfw/
    python pesquisa/preparar_dataset.py --fonte lfw --min_fotos_por_pessoa 15

    # Teste rapido so para validar o pipeline -> pesquisa/dados/att/
    python pesquisa/preparar_dataset.py --fonte att

Depois de gerado, rode:
    python pesquisa/benchmark_reconhecimento_facial.py --pares_por_pessoa 2
------------------------------------------------------------------------
"""

import argparse
import logging
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import numpy as np

logger = logging.getLogger(__name__)

# Abaixo disso o benchmark tem pares negativos pouco variados.
MINIMO_PESSOAS_RECOMENDADO = 4
QUALIDADE_JPEG = 95

# Por padrao cada fonte vai para pesquisa/dados/<fonte>/, de qualquer diretorio.
PASTA_DADOS = Path(__file__).resolve().parent / "dados"


def nome_da_pasta(rotulo: int, nomes: Sequence[str] | None) -> str:
    """Nome da pasta da pessoa: o nome real (LFW) ou `pessoa_NNN` quando nao ha nome (AT&T)."""
    nome = nomes[rotulo] if nomes is not None else f"pessoa_{rotulo:03d}"
    return str(nome).replace(" ", "_")


def para_uint8(imagem: "np.ndarray") -> "np.ndarray":
    """Converte a imagem para 0-255; o scikit-learn as vezes entrega valores em 0-1."""
    if imagem.max() <= 1.0:
        return (imagem * 255).astype("uint8")
    return imagem.astype("uint8")


def salvar_pessoas(
    imagens: "np.ndarray",
    rotulos: "np.ndarray",
    nomes: Sequence[str] | None,
    saida_dir: str | Path,
) -> None:
    """Grava cada imagem em `saida_dir/<pessoa>/foto_NNNN.jpg`."""
    from PIL import Image

    for indice, (imagem, rotulo) in enumerate(zip(imagens, rotulos, strict=True)):
        pasta_pessoa = Path(saida_dir) / nome_da_pasta(rotulo, nomes)
        pasta_pessoa.mkdir(parents=True, exist_ok=True)
        # O Pillow deduz o modo (L ou RGB) pelo formato do array.
        Image.fromarray(para_uint8(imagem)).save(
            pasta_pessoa / f"foto_{indice:04d}.jpg", quality=QUALIDADE_JPEG
        )


def preparar_lfw(saida_dir: str, min_fotos_por_pessoa: int) -> None:
    from sklearn.datasets import fetch_lfw_people

    logger.info("Baixando LFW (pode levar alguns minutos na primeira vez, ~200MB)...")
    lfw = fetch_lfw_people(min_faces_per_person=min_fotos_por_pessoa, color=True, resize=1.0)
    n_pessoas = len(lfw.target_names)
    logger.info(
        "%d pessoas com >= %d fotos cada (%d imagens no total).",
        n_pessoas,
        min_fotos_por_pessoa,
        len(lfw.images),
    )
    if n_pessoas < MINIMO_PESSOAS_RECOMENDADO:
        logger.warning(
            "Poucas pessoas atendem esse minimo de fotos. "
            "Considere diminuir --min_fotos_por_pessoa (ex.: 10)."
        )
    salvar_pessoas(lfw.images, lfw.target, lfw.target_names, saida_dir)


def preparar_att(saida_dir: str) -> None:
    from sklearn.datasets import fetch_olivetti_faces

    logger.info("Baixando AT&T / Olivetti Faces...")
    att = fetch_olivetti_faces()
    logger.info("%d pessoas, %d imagens no total.", len(set(att.target)), len(att.images))
    salvar_pessoas(att.images, att.target, None, saida_dir)
    logger.warning(
        "O AT&T/Olivetti e um dataset pequeno, antigo e com condicoes "
        "muito controladas (fundo escuro uniforme, iluminacao de estudio, preto "
        "e branco). Use-o so para validar se o pipeline de benchmark esta "
        "funcionando - NAO como resultado final do TCC, pois nao e representativo "
        "das condicoes reais dentro de um onibus escolar rural."
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(
        description="Prepara um dataset publico de rostos para o benchmark"
    )
    parser.add_argument("--fonte", choices=["lfw", "att"], default="lfw")
    parser.add_argument(
        "--min_fotos_por_pessoa",
        type=int,
        default=15,
        help="So usado com --fonte lfw. Quanto maior, menos pessoas sobram, "
        "mas mais robusto o teste.",
    )
    parser.add_argument("--saida", help="Pasta de saida (padrao: pesquisa/dados/<fonte>/)")
    args = parser.parse_args()
    saida = args.saida or str(PASTA_DADOS / args.fonte)

    if args.fonte == "lfw":
        preparar_lfw(saida, args.min_fotos_por_pessoa)
    else:
        preparar_att(saida)

    logger.info("\nDataset pronto em: %s", saida)
    logger.info(
        "Agora rode: python pesquisa/benchmark_reconhecimento_facial.py --dataset_dir %s", saida
    )


if __name__ == "__main__":
    main()
