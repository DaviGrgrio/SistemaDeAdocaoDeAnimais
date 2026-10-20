#Importa módulos abc (AbstractBaseClass), enum para opções fixas e List para TypeHint

from abc import ABC, abstractmethod
from datetime import date
from enum import Enum
from typing import List, Optional

PORTES_VALIDOS = ("P", "M", "G")

# Cria uma lista de opções fixas para os Status do Animal
class StatusAnimal(Enum):
    DISPONIVEL = "Disponível"
    RESERVADO = "Reservado"
    ADOTADO = "Adotado"
    DEVOLVIDO = "Devolvido"
    QUARENTENA = "Quarentena"
    INADOTAVEL = "Inadotável"

# Cria uma lista de opções fixas para o Sexo
class SexoAnimal(Enum):
    MACHO = "Macho"
    FEMEA = "Fêmea"


class Animal(ABC):
    """Classe base abstrata para os animais do abrigo."""

    def __init__(
        self,
        id_animal: int,
        nome: str,
        sexo: SexoAnimal,
        idade_meses: int,
        porte: str,
        temperamento: List[str],
        status: StatusAnimal = StatusAnimal.DISPONIVEL,
        data_entrada: Optional[date] = None       
    ) -> None:
        self._id_animal = id_animal
        self.nome = nome
        self._sexo = sexo
        self.idade_meses = idade_meses
        self.porte = porte
        self._temperamento = list(temperamento)
        self._status = status
        self._data_entrada = data_entrada or date.today()

    #Decoradores

    @property
    def id_animal(self) -> int:
        return self._id_animal

    
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("O nome não pode ser vazio.")
        self._nome = valor.strip()
    

    @property
    def idade_meses(self) -> int:
        return self._idade_meses

    @idade_meses.setter
    def idade_meses(self, valor: int) -> None:
        if valor <0:
            raise ValueError("A idade em meses não pode ser negativa.")
        self._idade_meses = valor

    @property
    def porte(self) -> str:
        return self._porte

    @porte.setter
    def porte(self, valor: str) -> None:
        valor = valor.upper()
        if valor not in PORTES_VALIDOS:
            raise ValueError("Porte deve ser P, M ou G.")
        self._porte = valor

    @property
    def temperamento(self) -> List[str]:
        return list(self._temperamento)

    @property
    def status(self) -> StatusAnimal:
        return self._status

    @property
    def data_entrada(self) -> date:
        return self._data_entrada

    def alterar_status(self, novo_status: StatusAnimal) -> None:
        # As transições válidas entram na semana 4
        self._status = novo_status

    @abstractmethod
    def descrever_necessidades(self) -> str:
        """Resumo das necessidades específicas da espécie."""

    # ---------- métodos especiais ----------
    def __str__(self) -> str:
        return (f"{self._nome} ({type(self).__name__}, {self._idade_meses} meses, "
                f"porte {self._porte}, {self._status.value})")

    def __repr__(self) -> str:
        return (f"{type(self).__name__}(id={self._id_animal}, "
                f"nome={self._nome!r}, status={self._status.name})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Animal):
            return NotImplemented
        return self._id_animal == other._id_animal

    def __hash__(self) -> int:
        return hash(self._id_animal)

    def __lt__(self, other: "Animal") -> bool:
        if not isinstance(other, Animal):
            return NotImplemented
        return self._data_entrada < other._data_entrada
