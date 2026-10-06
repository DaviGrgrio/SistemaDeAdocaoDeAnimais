from typing import List
from models.animal import Animal, SexoAnimal, StatusAnimal

"""
Representa um gato no abrigo, herda da classe abstrata Animal
e possui atributos específicos de felinos
"""

class Gato(Animal):

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
        #Atributos específicos de Felinos
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
