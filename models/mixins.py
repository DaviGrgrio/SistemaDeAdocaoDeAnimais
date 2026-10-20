"""Mixins de comportamentos reutilizáveis."""

from datetime import date
from typing import Dict, List, Optional


class VacinavelMixin:
    """Agenda/registro de vacinas."""

    def __init__(self, *args, vacinas: Optional[List[Dict[str, str]]] = None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._vacinas: List[Dict[str, str]] = list(vacinas) if vacinas else []

    @property
    def vacinas(self) -> List[Dict[str, str]]:
        return list(self._vacinas)

    def vacinar(self, nome_vacina: str, data: Optional[date] = None) -> None:
        if not nome_vacina or not nome_vacina.strip():
            raise ValueError("Informe o nome da vacina.")
        self._vacinas.append(
            {"vacina": nome_vacina.strip(), "data": (data or date.today()).isoformat()}
        )
    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["vacinas"] = list(self._vacinas)
        return dados

class AdestravelMixin:
    """Nível de adestramento (0 a 5)."""

    NIVEL_MAXIMO = 5

    def __init__(self, *args, nivel_adestramento: int = 0, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if not 0 <= nivel_adestramento <= self.NIVEL_MAXIMO:
            raise ValueError("Nível de adestramento deve estar entre 0 e 5.")
        self._nivel_adestramento = nivel_adestramento

    @property
    def nivel_adestramento(self) -> int:
        return self._nivel_adestramento

    def treinar(self) -> int:
        """Sobe um nível de adestramento (até o máximo) e devolve o nível atual."""
        if self._nivel_adestramento < self.NIVEL_MAXIMO:
            self._nivel_adestramento += 1
        return self._nivel_adestramento

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados["nivel_adestramento"] = self.nivel_adestramento
        return dados
