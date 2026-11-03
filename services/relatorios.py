from collections import Counter
from datetime import datetime
from typing import Callable, Dict, List, Optional, Tuple

from models.animal import Animal, StatusAnimal
from services.compatibilidade import calcular_compatibilidade


def relatorio_disponiveis_adotados(animais: List[Animal]) -> str:
    disponiveis = [a for a in animais if a.status == StatusAnimal.DISPONIVEL]
    adotados = [a for a in animais if a.status == StatusAnimal.ADOTADO]
    linhas = [f"=== Disponíveis ({len(disponiveis)}) ==="]
    linhas += [f"  - {a}" for a in sorted(disponiveis, key=lambda a: a.id_animal)]
    linhas.append(f"=== Adotados ({len(adotados)}) ===")
    linhas += [f"  - {a} -> {a.adotante.nome if a.adotante else '?'}"
               for a in sorted(adotados, key=lambda a: a.id_animal)]
    return "\n".join(linhas)


def _evento_adocao(animal) -> Optional[dict]:
    return next((e for e in animal if e["tipo"] == "adocao"), None)


def top_adotaveis(animais, adotantes, pesos, n: int = 5) -> List[Tuple]:
    """Top N animais com maior média de compatibilidade entre todos os adotantes."""
    if not adotantes:
        return []
    medias = [(a, round(sum(calcular_compatibilidade(ad, a, pesos) for ad in adotantes)
                        / len(adotantes), 2))
              for a in animais]
    return sorted(medias, key=lambda x: -x[1])[:n]


def taxa_adocao_por(animais, chave: Callable) -> Dict[str, float]:
    """Taxa de adoção agrupada (ex.: chave=lambda a: type(a).__name__ ou a.porte)."""
    totais, adotados = Counter(), Counter()
    for a in animais:
        k = chave(a)
        totais[k] += 1
        if _evento_adocao(a):
            adotados[k] += 1
    return {k: adotados[k] / totais[k] for k in totais}


def tempo_medio_adocao_dias(animais) -> Optional[float]:
    dias = []
    for a in animais:
        ev = _evento_adocao(a)
        if ev:
            dias.append((datetime.fromisoformat(ev["data"]).date() - a.data_entrada).days)
    return sum(dias) / len(dias) if dias else None


def devolucoes_por_motivo(animais) -> Dict[str, int]:
    return dict(Counter(e["detalhe"] for a in animais for e in a if e["tipo"] == "devolucao"))
