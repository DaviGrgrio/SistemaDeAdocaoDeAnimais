# Importa Abstract Base Class, para classes abstratas
from abc import ABC



class Pessoa(ABC):
    """Base para pessoas do sistema"""
    
    def __init__(self, nome: str, idade: int):
        # Chama os @setters para validar os dados na criação da instância
        self.nome = nome 
        self.idade = idade

    # @property permite ler o a informação protegida de fora da classe
    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor:str) -> None:
        """Valida nome da pessoa"""
        if not valor or not valor.strip():
            raise ValueError("O nome não pode ser vazio.")
        self._nome = valor.strip()
        
    @property
    def idade(self) -> int:
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        """Valida idade da pessoa"""
        if valor < 0:
            raise ValueError("A idade não pode ser negativa.")
        self._idade = valor
