from models.adotante import Adotante
from models.animal import SexoAnimal
from models.cachorro import Cachorro
from models.gato import Gato
from repositories.repositorio_json import RepositorioJSON


def popular(pasta: str = "data") -> None:
    """Grava dados de exemplo (apaga reservas e filas anteriores)."""
    animais = [
        Cachorro(1, "Rex", SexoAnimal.MACHO, 24, "M", ["calmo"], "SRD", "alta"),
        Cachorro(2, "Thor", SexoAnimal.MACHO, 6, "G", ["energético"], "Labrador", "alta"),
        Gato(3, "Mia", SexoAnimal.FEMEA, 10, "P", ["arisca"], 4, True, True),
        Gato(4, "Nina", SexoAnimal.FEMEA, 120, "P", ["dócil"], 5, True, True),
    ]
    adotantes = [
        Adotante(1, "Ana", 30, "casa", 80.0, True, False, False),
        Adotante(2, "Bia", 25, "apto", 40.0, False, True, False),
    ]
    repo = RepositorioJSON(pasta)
    repo.salvar(animais, adotantes)
    repo.salvar_estado({})


if __name__ == "__main__":
    popular()
    print("Dados de exemplo criados em data/.")
