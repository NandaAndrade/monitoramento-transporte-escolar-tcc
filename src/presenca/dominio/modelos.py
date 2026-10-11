"""Modelos do dominio: identificacoes vindas do reconhecedor e eventos de presenca."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TipoEvento(Enum):
    EMBARQUE = "embarque"
    DESEMBARQUE = "desembarque"
    ALERTA_DESCONHECIDO = "alerta_desconhecido"
    ALERTA_BAIXA_CONFIANCA = "alerta_baixa_confianca"


@dataclass(frozen=True)
class Identificacao:
    """Resultado do reconhecedor para um rosto encontrado no quadro.

    `aluno_id` e None quando o rosto nao se parece com nenhum aluno da galeria.
    """

    aluno_id: str | None
    confianca: float


@dataclass(frozen=True)
class Evento:
    """Evento de presenca ou alerta: e o que vai para a fila e para o TRANSCOLAR RURAL.

    O `id` (UUID4) e gerado na criacao e garante a idempotencia do envio (RF-08).
    """

    tipo: TipoEvento
    onibus_id: str
    rota_id: str
    momento: datetime
    aluno_id: str | None = None
    confianca: float | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
