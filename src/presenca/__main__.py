"""Composition root: monta os adaptadores concretos e roda o laco principal.

USO:
    python -m presenca --config config/dispositivo.toml
"""

import argparse
import logging
import time
from datetime import timedelta

from presenca.adaptadores.camera_opencv import CameraOpenCV
from presenca.adaptadores.fila_sqlite import FilaSqlite
from presenca.adaptadores.publicador_mqtt import PublicadorMqtt
from presenca.adaptadores.reconhecedor_deepface import ReconhecedorDeepFace
from presenca.adaptadores.relogio_sistema import RelogioSistema
from presenca.casos_uso.registrar_passagem import RegistrarPassagem
from presenca.casos_uso.sincronizar_eventos import SincronizarEventos
from presenca.config import Configuracao, carregar_configuracao
from presenca.dominio.passagens import ControlePassagens

logger = logging.getLogger(__name__)

# Pausa depois de um erro inesperado, para um erro persistente nao encher o log.
_ESPERA_APOS_ERRO_S = 1.0


def montar(config: Configuracao) -> tuple[RegistrarPassagem, SincronizarEventos]:
    fila = FilaSqlite(config.fila_arquivo)
    controle = ControlePassagens(
        onibus_id=config.onibus_id,
        rota_id=config.rota_id,
        confianca_minima=config.confianca_minima,
        intervalo_passagem=timedelta(seconds=config.intervalo_passagem_s),
    )
    registrar = RegistrarPassagem(
        camera=CameraOpenCV(config.camera_indice, config.camera_espera_maxima_s),
        reconhecedor=ReconhecedorDeepFace(config.galeria_dir, config.modelo, config.detector),
        controle=controle,
        fila=fila,
        relogio=RelogioSistema(),
    )
    publicador = PublicadorMqtt(
        config.mqtt_host, config.mqtt_porta, config.mqtt_topico, config.mqtt_timeout_s
    )
    return registrar, SincronizarEventos(fila, publicador)


def rodar(config: Configuracao) -> None:
    """Laco principal. Um erro inesperado e registrado e o laco continua.

    Os adaptadores ja tratam as falhas esperadas (quadro ruim, camera fora, rede
    fora); isto e so a rede de seguranca para que o onibus nao pare de registrar
    alunos por causa de um erro que ninguem previu.
    """
    registrar, sincronizar = montar(config)
    proxima_sincronizacao = 0.0
    while True:
        try:
            registrar.executar()
            if time.monotonic() >= proxima_sincronizacao:
                enviados = sincronizar.executar()
                if enviados:
                    logger.info("%d eventos sincronizados", enviados)
                proxima_sincronizacao = time.monotonic() + config.periodo_sincronizacao_s
        except Exception:
            logger.exception("Erro inesperado no laco principal; continuando")
            time.sleep(_ESPERA_APOS_ERRO_S)


def main() -> None:
    parser = argparse.ArgumentParser(description="Monitoramento de presenca no onibus escolar")
    parser.add_argument("--config", default="config/dispositivo.toml")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    try:
        rodar(carregar_configuracao(args.config))
    except KeyboardInterrupt:
        logger.info("Encerrado pelo usuario")


if __name__ == "__main__":
    main()
