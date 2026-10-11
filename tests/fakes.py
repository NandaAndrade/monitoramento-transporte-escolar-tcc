"""Implementacoes falsas das portas, para testar dominio e casos de uso sem hardware."""

from datetime import UTC, datetime, timedelta

from presenca.dominio.modelos import Evento, Identificacao
from presenca.portas import Quadro


class CameraFake:
    def __init__(self, quadros: list[Quadro | None]) -> None:
        self._quadros = list(quadros)

    def capturar(self) -> Quadro | None:
        return self._quadros.pop(0) if self._quadros else None


class ReconhecedorFake:
    """Devolve, para cada quadro, a lista de identificacoes associada a ele."""

    def __init__(self, respostas: dict[Quadro, list[Identificacao]]) -> None:
        self._respostas = respostas

    def identificar(self, quadro: Quadro) -> list[Identificacao]:
        return self._respostas.get(quadro, [])


class FilaFake:
    def __init__(self) -> None:
        self.eventos: dict[str, Evento] = {}
        self.enviados: set[str] = set()

    def adicionar(self, evento: Evento) -> None:
        self.eventos.setdefault(evento.id, evento)

    def pendentes(self, limite: int) -> list[Evento]:
        return [e for i, e in self.eventos.items() if i not in self.enviados][:limite]

    def marcar_enviado(self, evento_id: str) -> None:
        self.enviados.add(evento_id)


class PublicadorFake:
    """Aceita os `aceitar` primeiros envios e recusa os seguintes (simula queda de rede)."""

    def __init__(self, aceitar: int = 10**9) -> None:
        self._aceitar = aceitar
        self.publicados: list[Evento] = []

    def publicar(self, evento: Evento) -> bool:
        if len(self.publicados) >= self._aceitar:
            return False
        self.publicados.append(evento)
        return True


class RelogioFake:
    def __init__(self, inicio: datetime | None = None) -> None:
        self.momento = inicio or datetime(2026, 10, 11, 7, 0, tzinfo=UTC)

    def agora(self) -> datetime:
        return self.momento

    def avancar(self, segundos: float) -> None:
        self.momento += timedelta(seconds=segundos)
