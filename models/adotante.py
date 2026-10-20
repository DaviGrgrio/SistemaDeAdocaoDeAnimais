from models.pessoa import Pessoa

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
