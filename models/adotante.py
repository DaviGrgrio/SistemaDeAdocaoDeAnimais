from typing import TYPE_CHECKING, List

from models.pessoa import Pessoa
from models.animal import Animal, StatusAnimal

MORADIAS_VALIDAS = ("casa", "apto", "sítio")

class Adotante(Pessoa):
    """Pessoas interessadas em adotar um animal"""
    def __init__(
        self,
        id_adotante: int,
        nome: str,
        idade: int,
        moradia: str,
        area_util: float,
        experiencia_pets: bool,
        criancas_em_casa: bool,
        outros_animais: bool,
    ) -> None:
    # Repassa nome e idade para a superclasse
        super().__init__(nome, idade)

    #Guarda atributos específicos da classe filha (Adotante)
        self._id_adotante = id_adotante
        self.moradia = moradia
        self.area_util = area_util
        self._experiencia_pets = experiencia_pets
        self._criancas_em_casa = criancas_em_casa
        self._outros_animais = outros_animais
        self._animais_adotados = []

    @property
    def id_adotante(self) -> int:
        return self._id_adotante

    @property
    def moradia(self) -> str:
        return self._moradia

    @moradia.setter
    def moradia(self, valor: str) -> None:
        """Valida Moradia"""
        valor = valor.strip().lower()
        if valor not in MORADIAS_VALIDAS:
            raise ValueError("Moradia deve ser 'casa', 'apto' ou 'sítio'")
        self._moradia = valor

    @property
    def area_util(self) -> float:
        return self._area_util

    @area_util.setter
    def area_util(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("A área útil deve ser positiva")
        self._area_util = valor
        
    @property
    def experiencia_pets(self) -> bool:
        return self._experiencia_pets


    @property
    def criancas_em_casa(self) -> bool:
        return self._criancas_em_casa

    @property
    def outros_animais(self) -> bool:
        return self._outros_animais

    @property
    def animais_adotados(self) -> List[Animal]:
        return list(self._animais_adotados)

    def vincular_animal(self, animal: Animal) -> None:
        """Liga os dois lados da relação"""
        if animal not in self._animais_adotados:
            self._animais_adotados.append(animal)
        animal.definir_adotante(self)

    def adotar(self, animal: Animal) -> None:
        if not self.validar_elegibilidade():
            raise ValueError("Adotante Não elegível.")
        if animal.status != StatusAnimal.DISPONIVEL:
            raise ValueError("Animal não está disponível para adoção.")
        animal.alterar_status(StatusAnimal.ADOTADO)
        self.vincular_animal(animal)
        
    def validar_elegibilidade(self) -> bool:
        """Regra mínima: adotante com 18 anos ou mais."""
        return self._idade >= 18   


    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Adotante):
            return NotImplemented
        return self._id_adotante == other._id_adotante

    def __hash__(self) -> int:
        return hash(self._id_adotante)

    def __str__(self) -> str:
        return f"{self._nome}, {self._idade} anos, mora em {self._moradia}"

    #Serialização
    def to_dict(self) -> dict:
        return {
            "id_adotante": self._id_adotante, "nome": self._nome, "idade": self._idade,
            "moradia": self._moradia, "area_util": self._area_util,
            "experiencia_pets": self._experiencia_pets,
            "criancas_em_casa": self._criancas_em_casa,
            "outros_animais": self._outros_animais,
            "animais_adotados_ids": [a.id_animal for a in self._animais_adotados],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Adotante":
        return cls(d["id_adotante"], d["nome"], d["idade"], d["moradia"], d["area_util"],
                   d["experiencia_pets"], d["criancas_em_casa"], d["outros_animais"])
