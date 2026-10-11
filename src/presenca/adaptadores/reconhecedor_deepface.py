"""Reconhecedor facial usando a biblioteca DeepFace (ArcFace por padrao).

E o adaptador de prototipo, escolhido pelo benchmark. Na versao embarcada ele deve
ser substituido por um adaptador TFLite/Hailo com a mesma interface `Reconhecedor`.

A galeria de referencia e uma pasta com uma subpasta por aluno (mesmo formato de
`pesquisa/dados/`). Os embeddings sao calculados uma vez, na inicializacao.
TODO (RNF-10): carregar templates criptografados em vez de imagens.
"""

import logging
from pathlib import Path

from presenca.dominio.modelos import Identificacao
from presenca.portas import Quadro

logger = logging.getLogger(__name__)

_EXTENSOES = {".jpg", ".jpeg", ".png"}


class ReconhecedorDeepFace:
    def __init__(self, galeria_dir: str | Path, modelo: str, detector: str) -> None:
        import numpy as np
        from deepface import DeepFace

        self._np = np
        self._deepface = DeepFace
        self._modelo = modelo
        self._detector = detector
        self._galeria = self._carregar_galeria(Path(galeria_dir))
        logger.info("Galeria carregada: %d alunos", len(self._galeria))

    def identificar(self, quadro: Quadro) -> list[Identificacao]:
        """Um quadro com problema vira "nenhum rosto", nunca uma excecao.

        Assim um quadro corrompido ou um erro passageiro do TensorFlow nao
        interrompe o registro dos proximos alunos. O log nao inclui o quadro (RF-05).
        """
        try:
            embeddings = self._embeddings(quadro)
        except Exception:  # o DeepFace nao tem uma hierarquia de excecoes propria
            logger.exception("Falha ao reconhecer o quadro; ele foi descartado")
            return []
        return [self._comparar_com_galeria(e) for e in embeddings]

    def _carregar_galeria(self, galeria_dir: Path) -> dict[str, list]:
        galeria = {}
        for pasta in sorted(p for p in galeria_dir.iterdir() if p.is_dir()):
            embeddings = [
                e
                for imagem in pasta.iterdir()
                if imagem.suffix.lower() in _EXTENSOES
                for e in self._embeddings(str(imagem))
            ]
            if embeddings:
                galeria[pasta.name] = embeddings
        return galeria

    def _embeddings(self, imagem) -> list:
        resultados = self._deepface.represent(
            img_path=imagem,
            model_name=self._modelo,
            detector_backend=self._detector,
            enforce_detection=False,
        )
        # Sem rosto detectado, o DeepFace devolve a imagem inteira com confianca 0.
        return [
            self._np.asarray(r["embedding"]) for r in resultados if r.get("face_confidence", 1) > 0
        ]

    def _comparar_com_galeria(self, embedding) -> Identificacao:
        melhor_aluno, melhor_similaridade = None, -1.0
        for aluno_id, referencias in self._galeria.items():
            similaridade = max(self._cosseno(embedding, r) for r in referencias)
            if similaridade > melhor_similaridade:
                melhor_aluno, melhor_similaridade = aluno_id, similaridade
        return Identificacao(aluno_id=melhor_aluno, confianca=float(melhor_similaridade))

    def _cosseno(self, a, b) -> float:
        np = self._np
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
