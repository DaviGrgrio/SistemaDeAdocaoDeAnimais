import json
from pathlib import Path
from typing import Optional

PADRAO = {
    "idade_minima": 18, "area_minima_porte_g": 50.0, "reserva_horas": 48,
    "taxa_padrao": "padrao",
    "pesos": {"porte_moradia": 0.3, "idade_energia": 0.25, "experiencia": 0.25, "criancas": 0.2},
}


class Settings:
    """Configurações do sistema, lidas de settings.json."""

    def __init__(self, dados: Optional[dict] = None) -> None:
        self._d = {**PADRAO, **(dados or {})}

    @classmethod
    def carregar(cls, caminho: str = "settings.json") -> "Settings":
        p = Path(caminho)
        if not p.exists():
            return cls()
        with open(p, encoding="utf-8") as f:
            return cls(json.load(f))

    @property
    def idade_minima(self) -> int: return self._d["idade_minima"]
    @property
    def area_minima_porte_g(self) -> float: return self._d["area_minima_porte_g"]
    @property
    def reserva_horas(self) -> int: return self._d["reserva_horas"]
    @property
    def taxa_padrao(self) -> str: return self._d["taxa_padrao"]
    @property
    def pesos(self) -> dict: return dict(self._d["pesos"])
