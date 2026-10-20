import json
from pathlib import Path
from typing import List, Tuple

from models.adotante import Adotante
from models.animal import Animal
from models.cachorro import Cachorro
from models.gato import Gato

_TIPOS = {"Cachorro": Cachorro, "Gato": Gato}


class RepositorioJSON:
    """Salva e carrega animais e adotantes em arquivos JSON."""

    def __init__(self, pasta: str = "data") -> None:
        self._pasta = Path(pasta)
        self._pasta.mkdir(parents=True, exist_ok=True)

    def salvar(self, animais: List[Animal], adotantes: List[Adotante]) -> None:
        self._escrever("animais.json", [a.to_dict() for a in animais])
        self._escrever("adotantes.json", [a.to_dict() for a in adotantes])

    def carregar(self) -> Tuple[List[Animal], List[Adotante]]:
        animais = [_TIPOS[d["tipo"]].from_dict(d) for d in self._ler("animais.json")]
        dados_adotantes = self._ler("adotantes.json")
        adotantes = [Adotante.from_dict(d) for d in dados_adotantes]

        por_id = {a.id_animal: a for a in animais}
        for adotante, d in zip(adotantes, dados_adotantes):
            for id_animal in d.get("animais_adotados_ids", []):
                adotante.vincular_animal(por_id[id_animal])
        return animais, adotantes

    def _escrever(self, nome: str, dados: list) -> None:
        with open(self._pasta / nome, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def _ler(self, nome: str) -> list:
        caminho = self._pasta / nome
        if not caminho.exists():
            return []
        with open(caminho, encoding="utf-8") as f:
            return json.load(f)
