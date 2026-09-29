#Importa módulos abc (AbstractBaseClass), enum para opções fixas e List para TypeHint

from abc import ABC
from enum import Enum
from typing import List

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

#Cria classe base abstrata para animais
class Animal(ABC):

    def __init__(
        self,
        id_animal: int,
        nome: str,
        sexo: SexoAnimal,
        idade_meses: int,
        porte: str,
        temperamento: List[str],
        status: StatusAnimal = StatusAnimal.DISPONIVEL        
    ):
        self._id_animal = id_animal
        self._nome = nome
        self._sexo = sexo
        self._idade_meses = idade_meses
        self._porte = porte
        self._temperamento = temperamento
        self._status = status

    @property
    def id_animal(self) -> int:
        return self._id_animal

    
    @property
    def nome(self) -> str:
        return self._nome

    
    @property
    def status(self) -> StatusAnimal:
        return self._status

    def alterar_status(self, novo_status: StatusAnimal) -> None:
        self._status = novo_status
