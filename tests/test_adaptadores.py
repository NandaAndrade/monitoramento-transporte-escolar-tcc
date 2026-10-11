"""Testes do comportamento de falha dos adaptadores, sem OpenCV nem DeepFace instalados.

Os adaptadores sao montados sem chamar o construtor (que importa as bibliotecas
pesadas), com os atributos internos substituidos por fakes.
"""

from pathlib import Path

import pytest

from presenca.adaptadores import camera_opencv
from presenca.adaptadores.camera_opencv import CameraOpenCV
from presenca.adaptadores.reconhecedor_deepface import ReconhecedorDeepFace
from presenca.config import carregar_configuracao


class _Cv2Error(Exception):
    pass


class _Cv2Fake:
    error = _Cv2Error


class _CapturaFake:
    """Devolve, em ordem, os resultados de `read()`; uma excecao na lista e lancada."""

    def __init__(self, leituras):
        self._leituras = list(leituras)

    def read(self):
        leitura = self._leituras.pop(0)
        if isinstance(leitura, Exception):
            raise leitura
        return leitura


def _camera(leituras, espera_maxima_s=4.0) -> CameraOpenCV:
    camera = CameraOpenCV.__new__(CameraOpenCV)
    camera._cv2 = _Cv2Fake
    camera._espera_maxima_s = espera_maxima_s
    camera._espera_s = 0.0
    camera._captura = _CapturaFake(leituras)
    return camera


@pytest.fixture
def esperas(monkeypatch):
    registradas = []
    monkeypatch.setattr(camera_opencv.time, "sleep", registradas.append)
    return registradas


def test_camera_sem_quadro_espera_cada_vez_mais_ate_o_limite(esperas):
    camera = _camera([(False, None)] * 5, espera_maxima_s=4.0)

    for _ in range(5):
        assert camera.capturar() is None

    assert esperas == [0.5, 1.0, 2.0, 4.0, 4.0]


def test_camera_volta_ao_normal_quando_entrega_quadro(esperas):
    camera = _camera([(False, None), (True, "quadro"), (False, None)])

    camera.capturar()
    assert camera.capturar() == "quadro"
    camera.capturar()

    assert esperas == [0.5, 0.5]


def test_erro_do_opencv_vira_quadro_vazio(esperas):
    camera = _camera([_Cv2Error("falha de leitura")])

    assert camera.capturar() is None


def test_erro_no_reconhecimento_descarta_o_quadro_sem_excecao():
    reconhecedor = ReconhecedorDeepFace.__new__(ReconhecedorDeepFace)

    def falhar(_quadro):
        raise ValueError("quadro corrompido")

    reconhecedor._embeddings = falhar

    assert reconhecedor.identificar("quadro") == []


def test_caminhos_relativos_sao_lidos_a_partir_da_pasta_da_configuracao(tmp_path, monkeypatch):
    pasta_config = tmp_path / "config"
    pasta_config.mkdir()
    exemplo = Path("config/exemplo.toml").read_text(encoding="utf-8")
    (pasta_config / "dispositivo.toml").write_text(exemplo, encoding="utf-8")
    monkeypatch.chdir(tmp_path.parent)  # roda de outro diretorio

    config = carregar_configuracao(pasta_config / "dispositivo.toml")

    assert config.galeria_dir == str((tmp_path / "pesquisa" / "dados" / "att").resolve())
    assert config.fila_arquivo == str((pasta_config / "eventos.sqlite3").resolve())
