from datetime import date
from typing import List, Optional

from models.animal import Animal, SexoAnimal, StatusAnimal
from models.mixins import AdestravelMixin, VacinavelMixin


class Cachorro(VacinavelMixin, AdestravelMixin, Animal):
    """
    Representa um cachorro no abrigo, herda da classe abstrata Animal
    e possui atributos específicos de caninos
    """
    def __init__(
        self,
        id_animal: int,
        nome: str,
        sexo: SexoAnimal,
        idade_meses: int,
        porte: str,
        temperamento: List[str],
        raca: str,
        necessidade_passeio: str,
        status: StatusAnimal = StatusAnimal.DISPONIVEL,
        data_entrada: Optional[date] = None,
        vacinas: Optional[list] = None,
        nivel_adestramento: int = 0,
    ) -> None:
        super().__init__(
            id_animal=id_animal,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            temperamento=temperamento,
            status=status,
            data_entrada=data_entrada,
            vacinas=vacinas,
            nivel_adestramento=nivel_adestramento,
        )

        self._raca = raca
        self._necessidade_passeio = necessidade_passeio


    @property
    def raca(self) -> str:
        return self._raca

    @property
    def necessidade_passeio(self) -> str:
        return self._necessidade_passeio

    @property
    def adestrado(self) -> bool:
        return self._nivel_adestramento > 0

    def descrever_necessidades(self) -> str:
        return f"Precisa de passeios com frequência {self._necessidade_passeio}."


    #Serialização
    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados.update(raca=self._raca, necessidade_passeio=self._necessidade_passeio)
        return dados

    @classmethod
    def from_dict(cls, d: dict) -> "Cachorro":
        return cls(**Animal._campos_base(d), raca=d["raca"],
                   necessidade_passeio=d["necessidade_passeio"],
                   vacinas=d.get("vacinas"),
                   nivel_adestramento=d.get("nivel_adestramento", 0))
