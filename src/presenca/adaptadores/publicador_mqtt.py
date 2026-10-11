"""Publicador MQTT (paho-mqtt 2.x) para o TRANSCOLAR RURAL.

Usa QoS 1 e so devolve True depois do PUBACK do broker. Como QoS 1 pode entregar
a mesma mensagem mais de uma vez, o backend deve descartar `id` repetido (RF-08).
TODO: TLS e autenticacao, quando o contrato com o TRANSCOLAR RURAL for definido.
"""

import logging

from presenca.adaptadores.serializacao import evento_para_json
from presenca.dominio.modelos import Evento

logger = logging.getLogger(__name__)

_QOS_PELO_MENOS_UMA_VEZ = 1


class PublicadorMqtt:
    def __init__(self, host: str, porta: int, topico: str, timeout_s: float) -> None:
        import paho.mqtt.client as mqtt

        self._topico = topico
        self._timeout_s = timeout_s
        self._cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # connect_async + loop_start: o cliente reconecta sozinho quando a rede volta.
        self._cliente.connect_async(host, porta)
        self._cliente.loop_start()

    def publicar(self, evento: Evento) -> bool:
        if not self._cliente.is_connected():
            return False
        try:
            info = self._cliente.publish(
                self._topico, evento_para_json(evento), qos=_QOS_PELO_MENOS_UMA_VEZ
            )
            info.wait_for_publish(timeout=self._timeout_s)
            return info.is_published()
        except (RuntimeError, ValueError, OSError):
            logger.exception("Falha ao publicar %s", evento.id)
            return False

    def fechar(self) -> None:
        self._cliente.loop_stop()
        self._cliente.disconnect()
