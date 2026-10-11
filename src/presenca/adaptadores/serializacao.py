"""Conversao de Evento para JSON e de volta, compartilhada pela fila e pelo publicador."""

import json
from datetime import UTC, datetime

from presenca.dominio.modelos import Evento, TipoEvento


def evento_para_json(evento: Evento) -> str:
    return json.dumps(
        {
            "id": evento.id,
            "tipo": evento.tipo.value,
            "onibus_id": evento.onibus_id,
            "rota_id": evento.rota_id,
            "momento": evento.momento.astimezone(UTC).isoformat(),
            "aluno_id": evento.aluno_id,
            "confianca": evento.confianca,
        }
    )


def evento_de_json(texto: str) -> Evento:
    dados = json.loads(texto)
    return Evento(
        id=dados["id"],
        tipo=TipoEvento(dados["tipo"]),
        onibus_id=dados["onibus_id"],
        rota_id=dados["rota_id"],
        momento=datetime.fromisoformat(dados["momento"]),
        aluno_id=dados["aluno_id"],
        confianca=dados["confianca"],
    )
