from typing import List
from models.animal import Animal, SexoAnimal, StatusAnimal

"""
Representa um cachorro no abrigo, herda da classe abstrata Animal
e possui atributos específicos de caninos
"""
class Cachorro(Animal):

    def __init__(
        self,
        id_animal: int,
        nome: str,
        sexo: SexoAnimal,
        idade_meses: int,
        porte: str,
        temperamento: List[str],
        raca: str,
        adestrado: bool,
        necessidade_passeio: str,
        status: StatusAnimal = StatusAnimal.DISPONIVEL
    ) -> None:
        super().__init__(
            id_animal=id_animal,
            nome=nome,
            sexo=sexo,
            idade_meses=idade_meses,
            porte=porte,
            temperamento=temperamento,
            status=status,
        )

        self._raca = raca
        self._adestrado = adestrado
        self._necessidade_passeio = necessidade_passeio


    @property
    def raca(self) -> str:
        return self._raca

    @property
    def adestrado(self) -> bool:
        return self._adestrado

    @property
    def temperamento(self) -> List[str]:
        return self._temperamento
