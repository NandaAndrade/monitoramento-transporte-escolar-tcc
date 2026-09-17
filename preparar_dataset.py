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
