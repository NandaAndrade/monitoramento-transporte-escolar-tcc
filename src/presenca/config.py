"""Leitura da configuracao do dispositivo a partir de um arquivo TOML."""

import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Configuracao:
    onibus_id: str
    rota_id: str
    confianca_minima: float
    intervalo_passagem_s: float
    modelo: str
    detector: str
    galeria_dir: str
    camera_indice: int
    camera_espera_maxima_s: float
    fila_arquivo: str
    mqtt_host: str
    mqtt_porta: int
    mqtt_topico: str
    mqtt_timeout_s: float
    periodo_sincronizacao_s: float


def _resolver(caminho: str, pasta_config: Path) -> str:
    """Caminho relativo e lido a partir da pasta do arquivo de configuracao.

    Assim o dispositivo encontra a galeria e a fila mesmo rodando como servico,
    de qualquer diretorio de trabalho.
    """
    return str((pasta_config / caminho).resolve())


def carregar_configuracao(arquivo: str | Path) -> Configuracao:
    with open(arquivo, "rb") as f:
        dados = tomllib.load(f)
    pasta_config = Path(arquivo).resolve().parent
    dispositivo = dados["dispositivo"]
    reconhecimento = dados["reconhecimento"]
    mqtt = dados["mqtt"]
    return Configuracao(
        onibus_id=dispositivo["onibus_id"],
        rota_id=dispositivo["rota_id"],
        confianca_minima=reconhecimento["confianca_minima"],
        intervalo_passagem_s=reconhecimento["intervalo_passagem_s"],
        modelo=reconhecimento["modelo"],
        detector=reconhecimento["detector"],
        galeria_dir=_resolver(reconhecimento["galeria_dir"], pasta_config),
        camera_indice=dados["camera"]["indice"],
        camera_espera_maxima_s=dados["camera"]["espera_maxima_s"],
        fila_arquivo=_resolver(dados["fila"]["arquivo"], pasta_config),
        mqtt_host=mqtt["host"],
        mqtt_porta=mqtt["porta"],
        mqtt_topico=mqtt["topico"].format(onibus_id=dispositivo["onibus_id"]),
        mqtt_timeout_s=mqtt["timeout_s"],
        periodo_sincronizacao_s=dados["sincronizacao"]["periodo_s"],
    )
