"""Fila local de eventos em SQLite (store-and-forward).

Sobrevive a quedas de energia e a reinicios do dispositivo. O `id` do evento e
unico, entao gravar o mesmo evento duas vezes nao o duplica (RF-08). Um evento
confirmado e apagado: o dispositivo so guarda o que ainda nao foi enviado (RNF-16).
"""

import sqlite3
from pathlib import Path

from presenca.adaptadores.serializacao import evento_de_json, evento_para_json
from presenca.dominio.modelos import Evento

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS eventos (
    seq      INTEGER PRIMARY KEY AUTOINCREMENT,
    id       TEXT NOT NULL UNIQUE,
    payload  TEXT NOT NULL
)
"""


class FilaSqlite:
    def __init__(self, arquivo: str | Path) -> None:
        self._conexao = sqlite3.connect(arquivo)
        self._conexao.execute(_ESQUEMA)
        self._conexao.commit()

    def adicionar(self, evento: Evento) -> None:
        with self._conexao:
            self._conexao.execute(
                "INSERT OR IGNORE INTO eventos (id, payload) VALUES (?, ?)",
                (evento.id, evento_para_json(evento)),
            )

    def pendentes(self, limite: int) -> list[Evento]:
        linhas = self._conexao.execute(
            "SELECT payload FROM eventos ORDER BY seq LIMIT ?", (limite,)
        ).fetchall()
        return [evento_de_json(payload) for (payload,) in linhas]

    def confirmar_envio(self, evento_id: str) -> None:
        with self._conexao:
            self._conexao.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))

    def fechar(self) -> None:
        self._conexao.close()
