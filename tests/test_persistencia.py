import pytest
from models.animal import SexoAnimal, StatusAnimal
from models.adotante import Adotante
from models.cachorro import Cachorro
from models.gato import Gato
from repositories.repositorio_json import RepositorioJSON
from services.relatorios import relatorio_disponiveis_adotados


def montar():
    c = Cachorro(1, "Rex", SexoAnimal.MACHO, 24, "M", ["calmo"], "SRD", "alta")
    c.vacinar("V10"); c.treinar()
    g = Gato(2, "Mia", SexoAnimal.FEMEA, 10, "P", ["arisca"], 4, True, True)
    ana = Adotante(1, "Ana", 30, "casa", 80.0, True, False, False)
    return c, g, ana




def test_salvar_e_carregar_preserva_dados(tmp_path):
    c, g, ana = montar()
    c.alterar_status(StatusAnimal.RESERVADO)
    c.alterar_status(StatusAnimal.ADOTADO)
    ana.vincular_animal(c)
    repo = RepositorioJSON(tmp_path)
    repo.salvar([c, g], [ana])
    animais, adotantes = repo.carregar()

    assert len(animais) == 2 and len(adotantes) == 1
    rex = next(a for a in animais if a.nome == "Rex")
    assert isinstance(rex, Cachorro) and rex.nivel_adestramento == 1
    assert len(rex.vacinas) == 1
    assert rex.status == StatusAnimal.ADOTADO
    assert rex.adotante.nome == "Ana"


def test_carregar_sem_arquivos_devolve_vazio(tmp_path):
    assert RepositorioJSON(tmp_path).carregar() == ([], [])


def test_relatorio_lista_disponiveis_e_adotados():
    c, g, ana = montar()
    c.alterar_status(StatusAnimal.RESERVADO)
    c.alterar_status(StatusAnimal.ADOTADO)
    ana.vincular_animal(c)
    texto = relatorio_disponiveis_adotados([c, g])
    assert "Disponíveis (1)" in texto and "Adotados (1)" in texto
