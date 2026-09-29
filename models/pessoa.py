# Importa Abstract Base Class, para classes abstratas
from abc import ABC


# Cria o "molde" base da Pessoa 
class Pessoa(ABC):
    def __init__(self, nome: str, idade: int):
        self._nome = nome     # Variável protegida (tem '_')
        self._idade = idade   # Variável protegida (tem '_')

    # @property permite ler o a informação protegida de fora da classe
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def idade(self) -> int:
        return self._idade
