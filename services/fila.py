from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from models.adotante import Adotante
from models.excecoes import ReservaInvalidaError


@dataclass
class EntradaFila:
    adotante: Adotante
    pontuacao: float
    entrada_em: datetime

    def __lt__(self, other: "EntradaFila") -> bool:
        """Maior pontuação primeiro; empate: quem entrou antes."""
        return (-self.pontuacao, self.entrada_em) < (-other.pontuacao, other.entrada_em)


class FilaEspera:
    """Fila de espera priorizada por pontuação e tempo de espera."""

    def __init__(self) -> None:
        self._entradas: List[EntradaFila] = []

    def __len__(self) -> int:
        return len(self._entradas)

    @property
    def entradas(self) -> List[EntradaFila]:
        return list(self._entradas)

    def adicionar(self, adotante: Adotante, pontuacao: float, quando: Optional[datetime] = None) -> None:
        if any(e.adotante == adotante for e in self._entradas):
            raise ReservaInvalidaError("Adotante já está na fila.")
        self._entradas.append(EntradaFila(adotante, pontuacao, quando or datetime.now()))
        self._entradas.sort()

    def proximo(self) -> Optional[EntradaFila]:
        return self._entradas.pop(0) if self._entradas else None
