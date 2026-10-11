"""Fila local de eventos em SQLite (store-and-forward).

Sobrevive a quedas de energia e a reinicios do dispositivo. O `id` do evento e a
chave primaria, entao gravar o mesmo evento duas vezes nao o duplica (RF-08).
"""

import sqlite3
from pathlib import Path

from presenca.adaptadores.serializacao import evento_de_json, evento_para_json
from presenca.dominio.modelos import Evento

_ESQUEMA = """
CREATE TABLE IF NOT EXISTS eventos (
    seq      INTEGER PRIMARY KEY AUTOINCREMENT,
    id       TEXT NOT NULL UNIQUE,
    payload  TEXT NOT NULL,
    enviado  INTEGER NOT NULL DEFAULT 0
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
            "SELECT payload FROM eventos WHERE enviado = 0 ORDER BY seq LIMIT ?", (limite,)
        ).fetchall()
        return [evento_de_json(payload) for (payload,) in linhas]

    def marcar_enviado(self, evento_id: str) -> None:
        with self._conexao:
            self._conexao.execute("UPDATE eventos SET enviado = 1 WHERE id = ?", (evento_id,))

    def fechar(self) -> None:
        self._conexao.close()
