"""Testes das partes puras dos scripts de pesquisa (sem DeepFace nem download)."""

import queue

import pytest

from benchmark_reconhecimento_facial import (
    MatrizConfusao,
    aguardar_resultado,
    calcular_resultado,
    caminho_no_cache,
    gravar_tempos_deteccao,
    ler_tempos_deteccao,
    media_tempos_deteccao,
    montar_pares,
)
from preparar_dataset import nome_da_pasta


@pytest.fixture
def dataset(tmp_path):
    for pessoa in ["ana", "bia", "caio"]:
        pasta = tmp_path / pessoa
        pasta.mkdir()
        for i in range(3):
            (pasta / f"foto_{i}.jpg").touch()
    (tmp_path / "so_uma_foto").mkdir()
    (tmp_path / "so_uma_foto" / "foto_0.jpg").touch()
    return tmp_path


def test_pares_balanceados_entre_positivos_e_negativos(dataset):
    pares = montar_pares(dataset, pares_por_pessoa=2)

    positivos = [p for p in pares if p.mesma_pessoa]
    assert len(positivos) == 6
    assert len(pares) == 12


def test_pessoa_com_uma_foto_fica_de_fora(dataset):
    pares = montar_pares(dataset, pares_por_pessoa=2)

    assert all("so_uma_foto" not in p.img1 and "so_uma_foto" not in p.img2 for p in pares)


def test_mesma_semente_gera_os_mesmos_pares(dataset):
    assert montar_pares(dataset, 2, seed=7) == montar_pares(dataset, 2, seed=7)


def test_dataset_com_uma_pessoa_e_rejeitado(tmp_path):
    (tmp_path / "ana").mkdir()
    for i in range(2):
        (tmp_path / "ana" / f"foto_{i}.jpg").touch()

    with pytest.raises(ValueError):
        montar_pares(tmp_path, 2)


def test_metricas_calculadas_a_partir_da_matriz_de_confusao():
    matriz = MatrizConfusao()
    for esperado, previsto in [(True, True), (True, True), (True, False), (False, False)]:
        matriz.registrar(esperado, previsto)

    resultado = calcular_resultado("ArcFace", matriz, tempos=[0.5, 1.5], erros=1)

    assert resultado.acuracia == 0.75
    assert resultado.precisao == 1.0
    assert resultado.recall == 0.6667
    assert resultado.tempo_medio_s == 1.0
    assert resultado.tamanho_aprox_mb == 130


def test_modelo_sem_pares_avaliados_tem_metricas_vazias():
    resultado = calcular_resultado("SFace", MatrizConfusao(), tempos=[], erros=5)

    assert resultado.acuracia is None
    assert resultado.erros == 5


def test_recorte_no_cache_mantem_pessoa_e_nome_da_foto(tmp_path):
    destino = caminho_no_cache(str(tmp_path / "lfw" / "ana" / "foto_1.jpg"), tmp_path / "cache")

    assert destino == tmp_path / "cache" / "ana" / "foto_1.jpg"


def test_nome_da_pasta_usa_nome_real_ou_numero():
    assert nome_da_pasta(0, ["Abdullah Gul"]) == "Abdullah_Gul"
    assert nome_da_pasta(7, None) == "pessoa_007"


class _FilaFake:
    """Simula a fila do multiprocessing: cada item e um resultado ou `queue.Empty`."""

    def __init__(self, respostas):
        self._respostas = list(respostas)

    def get(self, timeout=None):
        resposta = self._respostas.pop(0) if self._respostas else queue.Empty()
        if isinstance(resposta, Exception):
            raise resposta
        return resposta

    def get_nowait(self):
        return self.get()


class _ProcessoFake:
    def __init__(self, vivo_por):
        self._vivo_por = vivo_por

    def is_alive(self):
        self._vivo_por -= 1
        return self._vivo_por >= 0


def test_processo_que_morre_sem_resultado_nao_trava():
    assert aguardar_resultado(_FilaFake([]), _ProcessoFake(vivo_por=2), 0) is None


def test_resultado_enviado_logo_antes_de_o_processo_morrer_e_aproveitado():
    fila = _FilaFake([queue.Empty(), {"modelo": "ArcFace"}])

    assert aguardar_resultado(fila, _ProcessoFake(vivo_por=0), 0) == {"modelo": "ArcFace"}


def test_media_de_deteccao_inclui_imagens_que_vieram_do_cache(tmp_path):
    gravar_tempos_deteccao(tmp_path, {"ana/foto_1.jpg": 1.0, "bia/foto_2.jpg": 3.0})
    imagens = ["lfw/ana/foto_1.jpg", "lfw/bia/foto_2.jpg", "lfw/caio/sem_tempo.jpg"]

    assert media_tempos_deteccao(ler_tempos_deteccao(tmp_path), imagens) == 2.0


def test_cache_sem_tempos_registrados_tem_media_vazia(tmp_path):
    assert media_tempos_deteccao(ler_tempos_deteccao(tmp_path), ["lfw/ana/foto.jpg"]) is None
