"""Decide, a partir de uma identificacao, se houve embarque, desembarque ou alerta."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from presenca.dominio.modelos import Evento, Identificacao, TipoEvento


@dataclass
class ControlePassagens:
    """Mantem quem esta a bordo e transforma identificacoes em eventos.

    O mesmo rosto aparece em muitos quadros seguidos; por isso o mesmo aluno (ou o
    mesmo tipo de alerta) so gera um novo evento depois de `intervalo_passagem`.
    """

    onibus_id: str
    rota_id: str
    confianca_minima: float
    intervalo_passagem: timedelta
    a_bordo: set[str] = field(default_factory=set)
    _ultimo_evento: dict[str, datetime] = field(default_factory=dict)

    def avaliar(self, identificacao: Identificacao, agora: datetime) -> Evento | None:
        """Devolve o evento gerado pela identificacao, ou None se ela deve ser ignorada."""
        tipo, chave = self._classificar(identificacao)
        if self._aconteceu_recentemente(chave, agora):
            return None
        self._ultimo_evento[chave] = agora
        if tipo is None:
            tipo = self._alternar_a_bordo(chave)
        return Evento(
            tipo=tipo,
            onibus_id=self.onibus_id,
            rota_id=self.rota_id,
            momento=agora,
            aluno_id=identificacao.aluno_id,
            confianca=identificacao.confianca,
        )

    def _classificar(self, identificacao: Identificacao) -> tuple[TipoEvento | None, str]:
        """Devolve (tipo de alerta, chave) ou (None, aluno_id) para uma passagem valida."""
        if identificacao.aluno_id is None:
            return TipoEvento.ALERTA_DESCONHECIDO, TipoEvento.ALERTA_DESCONHECIDO.value
        if identificacao.confianca < self.confianca_minima:
            tipo = TipoEvento.ALERTA_BAIXA_CONFIANCA
            return tipo, f"{tipo.value}:{identificacao.aluno_id}"
        return None, identificacao.aluno_id

    def _aconteceu_recentemente(self, chave: str, agora: datetime) -> bool:
        ultimo = self._ultimo_evento.get(chave)
        return ultimo is not None and agora - ultimo < self.intervalo_passagem

    def _alternar_a_bordo(self, aluno_id: str) -> TipoEvento:
        if aluno_id in self.a_bordo:
            self.a_bordo.remove(aluno_id)
            return TipoEvento.DESEMBARQUE
        self.a_bordo.add(aluno_id)
        return TipoEvento.EMBARQUE
