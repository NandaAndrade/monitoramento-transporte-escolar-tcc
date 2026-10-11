"""Relogio real do sistema operacional."""

from datetime import UTC, datetime


class RelogioSistema:
    def agora(self) -> datetime:
        return datetime.now(UTC)
