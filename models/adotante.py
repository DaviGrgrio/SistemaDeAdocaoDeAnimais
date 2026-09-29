from models.pessoa import Pessoa

class Adotante(Pessoa):

    def __init__(
        self,
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
        self._moradia = moradia
        self._area_util = area_util
        self._experiencia_pets = experiencia_pets
        self._criancas_em_casa = criancas_em_casa
        self._outros_animais = outros_animais

    @property
    def moradia(self) -> str:
        return self._moradia

    
    @property
    def experiencia_pets(self) -> bool:
        return self._experiencia_pets


    def validar_elegibilidade(self) -> bool:
        return self._idade >= 18   
