from services.config import Settings
from models.adotante import Adotante
from models.animal import Animal
from models.excecoes import PoliticaNaoAtendidaError


def validar_politica(adotante: Adotante, animal: Animal, settings: Settings) -> None:
    """Levanta PoliticaNaoAtendidaError se o adotante não puder adotar o animal."""
    if adotante.idade < settings.idade_minima:
        raise PoliticaNaoAtendidaError(f"Idade mínima do adotante: {settings.idade_minima} anos.")
    if animal.porte == "G" and (
        adotante.moradia != "casa" or adotante.area_util < settings.area_minima_porte_g
    ):
        raise PoliticaNaoAtendidaError(
            f"Porte G exige casa com área útil de pelo menos {settings.area_minima_porte_g} m²."
        )
