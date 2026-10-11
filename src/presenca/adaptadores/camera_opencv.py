"""Camera via OpenCV (webcam USB ou camera do Raspberry Pi exposta como /dev/video).

O quadro fica so em memoria: este adaptador nunca grava imagem (RF-05).
"""

import logging

from presenca.portas import Quadro

logger = logging.getLogger(__name__)


class CameraOpenCV:
    def __init__(self, indice: int = 0) -> None:
        import cv2

        self._captura = cv2.VideoCapture(indice)
        if not self._captura.isOpened():
            raise RuntimeError(f"Nao foi possivel abrir a camera {indice}")

    def capturar(self) -> Quadro | None:
        ok, quadro = self._captura.read()
        if not ok:
            logger.warning("Camera nao entregou quadro")
            return None
        return quadro

    def fechar(self) -> None:
        self._captura.release()
