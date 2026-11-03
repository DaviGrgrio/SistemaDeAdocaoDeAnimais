from typing import Dict, Type
from models.animal import Animal


class BaseFeeStrategy:
    """Taxa padrão de adoção. As subclasses ajustam o cálculo."""
    VALOR_BASE = 100.0

    def calcular(self, animal: Animal) -> float:
        return self.VALOR_BASE


class SeniorFee(BaseFeeStrategy):
    def calcular(self, animal: Animal) -> float:
        return super().calcular(animal) * 0.5  # desconto de 50%


class PuppyFee(BaseFeeStrategy):
    def calcular(self, animal: Animal) -> float:
        return super().calcular(animal) + 50.0  # custo das vacinas


class SpecialCareFee(BaseFeeStrategy):
    def calcular(self, animal: Animal) -> float:
        return super().calcular(animal) + 150.0  # tratamento


ESTRATEGIAS: Dict[str, Type[BaseFeeStrategy]] = {
    "padrao": BaseFeeStrategy, "senior": SeniorFee, "filhote": PuppyFee, "especial": SpecialCareFee,
}


def escolher_estrategia(animal: Animal, padrao: str = "padrao") -> BaseFeeStrategy:
    if any(e["tipo"] == "tratamento" for e in animal):
        return SpecialCareFee()
    if animal.idade_meses >= 96:
        return SeniorFee()
    if animal.idade_meses < 12:
        return PuppyFee()
    return ESTRATEGIAS[padrao]()
