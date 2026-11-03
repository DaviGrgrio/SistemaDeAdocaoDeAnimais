import pytest
from models.animal import Animal, SexoAnimal, StatusAnimal
from models.adotante import Adotante
from models.cachorro import Cachorro
from models.gato import Gato


def novo_cachorro(id_animal=1, **kw):
    base = dict(id_animal=id_animal, nome="Rex", sexo=SexoAnimal.MACHO, idade_meses=24,
                porte="M", temperamento=["calmo"], raca="SRD", necessidade_passeio="alta")
    base.update(kw)
    return Cachorro(**base)


def novo_adotante(**kw):
    base = dict(id_adotante=1, nome="Ana", idade=30, moradia="casa", area_util=80.0,
                experiencia_pets=True, criancas_em_casa=False, outros_animais=False)
    base.update(kw)
    return Adotante(**base)


def test_animal_abstrato_nao_instancia():
    with pytest.raises(TypeError):
        Animal(1, "X", SexoAnimal.MACHO, 1, "P", [])


def test_cachorro_criado_com_status_padrao():
    assert novo_cachorro().status == StatusAnimal.DISPONIVEL


def test_idade_negativa_invalida():
    with pytest.raises(ValueError):
        novo_cachorro(idade_meses=-1)


def test_porte_invalido():
    with pytest.raises(ValueError):
        novo_cachorro(porte="X")


def test_igualdade_por_id():
    assert novo_cachorro(1, nome="A") == novo_cachorro(1, nome="B")
    assert novo_cachorro(1) != novo_cachorro(2)


def test_str_contem_nome_e_tipo():
    assert "Rex" in str(novo_cachorro()) and "Cachorro" in str(novo_cachorro())


def test_vacinar_e_treinar():
    c = novo_cachorro()
    c.vacinar("V10")
    assert len(c.vacinas) == 1
    assert c.treinar() == 1


def test_gato_independencia_invalida():
    with pytest.raises(ValueError):
        Gato(1, "Mia", SexoAnimal.FEMEA, 10, "P", [], 9, True, True)


def test_adotante_menor_nao_elegivel():
    assert novo_adotante(idade=17).validar_elegibilidade() is False


def test_adotante_moradia_invalida():
    with pytest.raises(ValueError):
        novo_adotante(moradia="barraca")
