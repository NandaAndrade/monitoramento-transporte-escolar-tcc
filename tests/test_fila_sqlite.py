from datetime import UTC, datetime

from presenca.adaptadores.fila_sqlite import FilaSqlite
from presenca.dominio.modelos import Evento, TipoEvento


def _evento(aluno_id: str) -> Evento:
    return Evento(
        tipo=TipoEvento.EMBARQUE,
        onibus_id="onibus-01",
        rota_id="rota-01",
        momento=datetime(2026, 10, 11, 7, 0, tzinfo=UTC),
        aluno_id=aluno_id,
        confianca=0.9,
    )


def test_fila_preserva_ordem_e_conteudo(tmp_path):
    fila = FilaSqlite(tmp_path / "fila.sqlite3")
    a, b = _evento("ana"), _evento("bia")
    fila.adicionar(a)
    fila.adicionar(b)

    assert fila.pendentes(10) == [a, b]


def test_fila_ignora_evento_duplicado(tmp_path):
    fila = FilaSqlite(tmp_path / "fila.sqlite3")
    evento = _evento("ana")
    fila.adicionar(evento)
    fila.adicionar(evento)

    assert len(fila.pendentes(10)) == 1


def test_fila_sobrevive_a_reinicio(tmp_path):
    arquivo = tmp_path / "fila.sqlite3"
    fila = FilaSqlite(arquivo)
    evento = _evento("ana")
    fila.adicionar(evento)
    fila.fechar()

    reaberta = FilaSqlite(arquivo)
    assert reaberta.pendentes(10) == [evento]
    reaberta.marcar_enviado(evento.id)
    assert reaberta.pendentes(10) == []
