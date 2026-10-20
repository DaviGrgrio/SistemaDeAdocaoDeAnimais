from datetime import date
from typing import List, Optional

from models.animal import Animal, SexoAnimal, StatusAnimal
from models.mixins import VacinavelMixin


class Gato(VacinavelMixin, Animal):
    """
    Representa um gato no abrigo, herda da classe abstrata Animal
    e possui atributos específicos de felinos
    """
    
    def __init__(
        self,
        id_animal: int,
        nome: str,
        sexo: SexoAnimal,
        idade_meses: int,
        porte: str,
        temperamento: List[str],
        nivel_independencia: int,
        fiv_felv_negativo: bool,
        usa_caixa_areia: bool,
        status: StatusAnimal = StatusAnimal.DISPONIVEL,
        data_entrada: Optional[date] = None,
        vacinas: Optional[list] = None,
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
        )
        #Atributos específicos de Felinos
        if not 1 <= nivel_independencia <=5:
            raise ValueError("Nível de independência deve estar entre 1 e 5.")
        self._fiv_felv_negativo = fiv_felv_negativo
        self._usa_caixa_areia = usa_caixa_areia
        self._nivel_independencia = nivel_independencia

    @property
    def fiv_felv_negativo(self) -> bool:
        """Indica se o teste de FIV/FeLV deu negativo """
        return self._fiv_felv_negativo

    @property
    def usa_caixa_areia(self) -> bool:
        """Indica se o gato já utiliza a caixa de areia """
        return self._usa_caixa_areia

    @property
    def nivel_independencia(self) -> int:
        """Indica o nível de independência do gato"""
        return self._nivel_independencia

    def descrever_necessidades(self) -> str:
        return f"Gato com independência nível {self._nivel_independencia}/5."

    def to_dict(self) -> dict:
        dados = super().to_dict()
        dados.update(nivel_independencia=self._nivel_independencia,
                     fiv_felv_negativo=self._fiv_felv_negativo,
                     usa_caixa_areia=self._usa_caixa_areia)
        return dados

    @classmethod
    def from_dict(cls, d: dict) -> "Gato":
        return cls(**Animal._campos_base(d),
                   nivel_independencia=d["nivel_independencia"],
                   fiv_felv_negativo=d["fiv_felv_negativo"],
                   usa_caixa_areia=d["usa_caixa_areia"],
                   vacinas=d.get("vacinas"))
