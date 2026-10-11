"""Caso de uso: processar um quadro da camera e enfileirar os eventos gerados."""

import logging

from presenca.dominio.modelos import Evento
from presenca.dominio.passagens import ControlePassagens
from presenca.portas import Camera, FilaEventos, Reconhecedor, Relogio

logger = logging.getLogger(__name__)


class RegistrarPassagem:
    def __init__(
        self,
        camera: Camera,
        reconhecedor: Reconhecedor,
        controle: ControlePassagens,
        fila: FilaEventos,
        relogio: Relogio,
    ) -> None:
        self._camera = camera
        self._reconhecedor = reconhecedor
        self._controle = controle
        self._fila = fila
        self._relogio = relogio

    def executar(self) -> list[Evento]:
        """Captura um quadro, reconhece os rostos e grava os eventos na fila local."""
        quadro = self._camera.capturar()
        if quadro is None:
            return []
        agora = self._relogio.agora()
        eventos = []
        for identificacao in self._reconhecedor.identificar(quadro):
            evento = self._controle.avaliar(identificacao, agora)
            if evento is None:
                continue
            self._fila.adicionar(evento)
            logger.info("Evento %s: %s aluno=%s", evento.id, evento.tipo.value, evento.aluno_id)
            eventos.append(evento)
        return eventos
