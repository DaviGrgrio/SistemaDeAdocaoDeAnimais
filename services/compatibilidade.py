from typing import Dict
from models.adotante import Adotante
from models.animal import Animal


def _porte_moradia(ad: Adotante, an: Animal) -> float:
    if ad.moradia == "casa":
        return 100.0
    return {"P": 100.0, "M": 60.0, "G": 20.0}[an.porte]


def _idade_energia(ad: Adotante, an: Animal) -> float:
    if an.idade_meses < 12:  # filhote: muita energia
        return 100.0 if ad.experiencia_pets else 50.0
    return 80.0


def _experiencia(ad: Adotante, an: Animal) -> float:
    return 100.0 if ad.experiencia_pets else 50.0


def _criancas(ad: Adotante, an: Animal) -> float:
    if not ad.criancas_em_casa:
        return 100.0
    arisco = any("aris" in t.lower() for t in an.temperamento)
    return 20.0 if arisco else 70.0


def calcular_compatibilidade(ad: Adotante, an: Animal, pesos: Dict[str, float]) -> float:
    """Pontuação de 0 a 100 (soma ponderada dos critérios)."""
    criterios = {
        "porte_moradia": _porte_moradia(ad, an), "idade_energia": _idade_energia(ad, an),
        "experiencia": _experiencia(ad, an), "criancas": _criancas(ad, an),
    }
    total = sum(pesos.get(k, 0) for k in criterios)
    if total <= 0:
        raise ValueError("A soma dos pesos deve ser positiva.")
    return round(sum(pesos.get(k, 0) * v for k, v in criterios.items()) / total, 2)
