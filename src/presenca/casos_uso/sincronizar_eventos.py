"""Caso de uso: enviar os eventos pendentes da fila local ao TRANSCOLAR RURAL."""

import logging

from presenca.portas import FilaEventos, Publicador

logger = logging.getLogger(__name__)


class SincronizarEventos:
    def __init__(self, fila: FilaEventos, publicador: Publicador, lote: int = 50) -> None:
        self._fila = fila
        self._publicador = publicador
        self._lote = lote

    def executar(self) -> int:
        """Publica os pendentes em ordem e devolve quantos foram confirmados.

        Para no primeiro envio que falhar: sem rede nao adianta tentar o resto do
        lote, e manter a ordem facilita a leitura dos eventos no backend.
        """
        enviados = 0
        for evento in self._fila.pendentes(self._lote):
            if not self._publicador.publicar(evento):
                logger.warning("Envio falhou; %s fica na fila para a proxima tentativa", evento.id)
                break
            self._fila.marcar_enviado(evento.id)
            enviados += 1
        return enviados
