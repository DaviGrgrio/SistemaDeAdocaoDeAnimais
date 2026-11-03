import json
import os
from pathlib import Path
from typing import Any, List, Tuple

from models.adotante import Adotante
from models.animal import Animal
from models.cachorro import Cachorro
from models.excecoes import RepositorioError
from models.gato import Gato

_TIPOS = {"Cachorro": Cachorro, "Gato": Gato}


class RepositorioJSON:
    """Persiste animais, adotantes e o estado (reservas/filas) em arquivos JSON."""

    def __init__(self, pasta: str = "data") -> None:
        self._pasta = Path(pasta)
        self._pasta.mkdir(parents=True, exist_ok=True)

    def salvar(self, animais: List[Animal], adotantes: List[Adotante]) -> None:
        self._escrever("animais.json", [a.to_dict() for a in animais])
        self._escrever("adotantes.json", [a.to_dict() for a in adotantes])

    def carregar(self) -> Tuple[List[Animal], List[Adotante]]:
        dados_animais = self._ler("animais.json", [])
        animais = [_TIPOS[d["tipo"]].from_dict(d) for d in dados_animais]
        for a, d in zip(animais, dados_animais):
            a.restaurar_historico(d.get("historico", []))

        dados_adotantes = self._ler("adotantes.json", [])
        adotantes = [Adotante.from_dict(d) for d in dados_adotantes]
        por_id = {a.id_animal: a for a in animais}
        for adotante, d in zip(adotantes, dados_adotantes):
            for id_animal in d.get("animais_adotados_ids", []):
                adotante.vincular_animal(por_id[id_animal])
        return animais, adotantes

    def salvar_estado(self, estado: dict) -> None:
        self._escrever("estado.json", estado)

    def carregar_estado(self) -> dict:
        return self._ler("estado.json", {})

    def _escrever(self, nome: str, dados: Any) -> None:
        destino = self._pasta / nome
        temporario = destino.with_suffix(".tmp")
        try:
            with open(temporario, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            os.replace(temporario, destino)  # troca atômica: grava tudo ou nada
        except OSError as e:
            raise RepositorioError(f"Falha ao gravar {nome}: {e}") from e

    def _ler(self, nome: str, padrao: Any) -> Any:
        caminho = self._pasta / nome
        if not caminho.exists():
            return padrao
        try:
            with open(caminho, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise RepositorioError(f"Falha ao ler {nome}: {e}") from e
