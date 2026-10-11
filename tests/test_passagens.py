from datetime import UTC, datetime, timedelta

import pytest

from presenca.dominio.modelos import Identificacao, TipoEvento
from presenca.dominio.passagens import ControlePassagens

INICIO = datetime(2026, 10, 11, 7, 0, tzinfo=UTC)


@pytest.fixture
def controle() -> ControlePassagens:
    return ControlePassagens(
        onibus_id="onibus-01",
        rota_id="rota-01",
        confianca_minima=0.7,
        intervalo_passagem=timedelta(seconds=60),
    )


def test_primeira_passagem_e_embarque_e_a_segunda_e_desembarque(controle):
    ana = Identificacao("ana", 0.9)

    embarque = controle.avaliar(ana, INICIO)
    desembarque = controle.avaliar(ana, INICIO + timedelta(minutes=30))

    assert embarque.tipo is TipoEvento.EMBARQUE
    assert desembarque.tipo is TipoEvento.DESEMBARQUE
    assert controle.a_bordo == set()


def test_mesmo_aluno_em_quadros_seguidos_conta_uma_vez(controle):
    ana = Identificacao("ana", 0.9)

    controle.avaliar(ana, INICIO)

    assert controle.avaliar(ana, INICIO + timedelta(seconds=1)) is None
    assert controle.a_bordo == {"ana"}


def test_rosto_desconhecido_gera_alerta_sem_repetir_a_cada_quadro(controle):
    desconhecido = Identificacao(None, 0.0)

    alerta = controle.avaliar(desconhecido, INICIO)

    assert alerta.tipo is TipoEvento.ALERTA_DESCONHECIDO
    assert controle.avaliar(desconhecido, INICIO + timedelta(seconds=1)) is None


def test_baixa_confianca_gera_alerta_e_nao_muda_quem_esta_a_bordo(controle):
    evento = controle.avaliar(Identificacao("ana", 0.5), INICIO)

    assert evento.tipo is TipoEvento.ALERTA_BAIXA_CONFIANCA
    assert evento.aluno_id == "ana"
    assert controle.a_bordo == set()


def test_cada_evento_tem_id_unico(controle):
    a = controle.avaliar(Identificacao("ana", 0.9), INICIO)
    b = controle.avaliar(Identificacao("bia", 0.9), INICIO)

    assert a.id != b.id
