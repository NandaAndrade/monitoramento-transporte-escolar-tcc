"""Camera via OpenCV (webcam USB ou camera do Raspberry Pi exposta como /dev/video).

O quadro fica so em memoria: este adaptador nunca grava imagem (RF-05).
"""

import logging
import time

from presenca.portas import Quadro

logger = logging.getLogger(__name__)

_ESPERA_INICIAL_S = 0.5


class CameraOpenCV:
    """Camera que nunca derruba o laco principal.

    Se a camera para de entregar quadros (cabo solto, falha de leitura), cada
    tentativa seguinte espera o dobro da anterior, ate `espera_maxima_s`, em vez
    de girar a 100% de CPU. O aviso vai para o log uma vez por queda.
    """

    def __init__(self, indice: int, espera_maxima_s: float) -> None:
        import cv2

        self._cv2 = cv2
        self._espera_maxima_s = espera_maxima_s
        self._espera_s = 0.0
        self._captura = cv2.VideoCapture(indice)
        if not self._captura.isOpened():
            raise RuntimeError(f"Nao foi possivel abrir a camera {indice}")

    def capturar(self) -> Quadro | None:
        try:
            ok, quadro = self._captura.read()
        except self._cv2.error:
            logger.exception("Erro do OpenCV ao ler a camera")
            ok, quadro = False, None
        if ok:
            self._registrar_volta()
            return quadro
        self._esperar_antes_da_proxima_tentativa()
        return None

    def _registrar_volta(self) -> None:
        if self._espera_s:
            logger.info("Camera voltou a entregar quadros")
            self._espera_s = 0.0

    def _esperar_antes_da_proxima_tentativa(self) -> None:
        if not self._espera_s:
            logger.warning("Camera nao entregou quadro; tentando de novo com espera crescente")
        self._espera_s = min(max(self._espera_s * 2, _ESPERA_INICIAL_S), self._espera_maxima_s)
        time.sleep(self._espera_s)

    def fechar(self) -> None:
        self._captura.release()
