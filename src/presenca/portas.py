"""Portas: o que os casos de uso precisam do mundo externo.

Cada porta e um Protocol pequeno; os adaptadores em `presenca.adaptadores`
implementam essas interfaces sem precisar herdar delas.
"""

from datetime import datetime
from typing import Any, Protocol

from presenca.dominio.modelos import Evento, Identificacao

# O quadro e opaco para o dominio (na pratica, um array do OpenCV).
Quadro = Any


class Camera(Protocol):
    def capturar(self) -> Quadro | None:
        """Devolve o quadro atual, ou None se a camera nao entregou imagem."""
        ...


class Reconhecedor(Protocol):
    def identificar(self, quadro: Quadro) -> list[Identificacao]:
        """Devolve uma identificacao por rosto encontrado no quadro."""
        ...


class FilaEventos(Protocol):
    """Armazenamento local dos eventos ate a confirmacao do envio (store-and-forward)."""

    def adicionar(self, evento: Evento) -> None:
        """Grava o evento; um `id` ja existente e ignorado."""
        ...

    def pendentes(self, limite: int) -> list[Evento]:
        """Eventos ainda nao enviados, do mais antigo para o mais novo."""
        ...

    def marcar_enviado(self, evento_id: str) -> None: ...


class Publicador(Protocol):
    def publicar(self, evento: Evento) -> bool:
        """Envia o evento ao TRANSCOLAR RURAL. Devolve True somente apos a confirmacao."""
        ...


class Relogio(Protocol):
    def agora(self) -> datetime:
        """Momento atual, com fuso horario."""
        ...
