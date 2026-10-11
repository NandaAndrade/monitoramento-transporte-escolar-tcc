from datetime import timedelta

from presenca.casos_uso.registrar_passagem import RegistrarPassagem
from presenca.casos_uso.sincronizar_eventos import SincronizarEventos
from presenca.dominio.modelos import Identificacao, TipoEvento
from presenca.dominio.passagens import ControlePassagens
from tests.fakes import CameraFake, FilaFake, PublicadorFake, ReconhecedorFake, RelogioFake


def _controle() -> ControlePassagens:
    return ControlePassagens("onibus-01", "rota-01", 0.7, timedelta(seconds=60))


def test_registrar_passagem_grava_eventos_na_fila():
    fila = FilaFake()
    registrar = RegistrarPassagem(
        camera=CameraFake(["q1"]),
        reconhecedor=ReconhecedorFake(
            {"q1": [Identificacao("ana", 0.9), Identificacao(None, 0.1)]}
        ),
        controle=_controle(),
        fila=fila,
        relogio=RelogioFake(),
    )

    eventos = registrar.executar()

    assert [e.tipo for e in eventos] == [TipoEvento.EMBARQUE, TipoEvento.ALERTA_DESCONHECIDO]
    assert len(fila.eventos) == 2


def test_registrar_passagem_sem_quadro_nao_faz_nada():
    fila = FilaFake()
    registrar = RegistrarPassagem(
        CameraFake([None]), ReconhecedorFake({}), _controle(), fila, RelogioFake()
    )

    assert registrar.executar() == []
    assert fila.eventos == {}


def _fila_com_eventos(quantidade: int) -> FilaFake:
    fila, controle, relogio = FilaFake(), _controle(), RelogioFake()
    for i in range(quantidade):
        fila.adicionar(controle.avaliar(Identificacao(f"aluno{i}", 0.9), relogio.agora()))
    return fila


def test_sincronizar_envia_pendentes_e_apaga_os_confirmados():
    fila = _fila_com_eventos(3)
    publicador = PublicadorFake()

    assert SincronizarEventos(fila, publicador).executar() == 3
    assert fila.eventos == {}


def test_sincronizar_sem_rede_mantem_eventos_na_fila_e_retoma_depois():
    fila = _fila_com_eventos(3)

    assert SincronizarEventos(fila, PublicadorFake(aceitar=1)).executar() == 1
    assert len(fila.pendentes(10)) == 2

    assert SincronizarEventos(fila, PublicadorFake()).executar() == 2
    assert fila.pendentes(10) == []
