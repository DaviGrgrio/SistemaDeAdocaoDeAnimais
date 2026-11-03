from datetime import datetime, timedelta

import pytest

from services.compatibilidade import calcular_compatibilidade
from services.config import Settings
from services.fila import FilaEspera
from models.adotante import Adotante
from models.animal import SexoAnimal, StatusAnimal
from models.cachorro import Cachorro
from models.excecoes import (PoliticaNaoAtendidaError, ReservaInvalidaError,
                             TransicaoDeEstadoInvalidaError)
from services.relatorios import devolucoes_por_motivo, taxa_adocao_por
from services.servico import AdocaoService
from services.taxas import BaseFeeStrategy, PuppyFee, SeniorFee

T0 = datetime(2026, 11, 1, 10, 0)


def cenario(porte="M", idade_meses=24, temperamento=("calmo",)):
    rex = Cachorro(1, "Rex", SexoAnimal.MACHO, idade_meses, porte, list(temperamento), "SRD", "alta")
    ana = Adotante(1, "Ana", 30, "casa", 80.0, True, False, False)
    bia = Adotante(2, "Bia", 25, "apto", 40.0, False, True, False)
    return AdocaoService(Settings(), [rex], [ana, bia]), rex, ana, bia


def test_transicao_invalida():
    _, rex, _, _ = cenario()
    with pytest.raises(TransicaoDeEstadoInvalidaError):
        rex.alterar_status(StatusAnimal.ADOTADO)


def test_reservar_muda_status():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    assert rex.status == StatusAnimal.RESERVADO


def test_reserva_duplicada_falha():
    svc, rex, ana, bia = cenario()
    svc.reservar(ana, rex, T0)
    with pytest.raises(ReservaInvalidaError):
        svc.reservar(bia, rex, T0)


def test_menor_de_idade_violada_politica():
    svc, rex, _, _ = cenario()
    menor = Adotante(3, "Teo", 17, "casa", 80.0, True, False, False)
    with pytest.raises(PoliticaNaoAtendidaError):
        svc.reservar(menor, rex, T0)


def test_porte_g_exige_casa_com_area():
    svc, rex, _, bia = cenario(porte="G")
    with pytest.raises(PoliticaNaoAtendidaError):
        svc.reservar(bia, rex, T0)


def test_reserva_expira_apos_48h():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    assert svc.rodar_expiracao(T0 + timedelta(hours=47)) == []
    assert rex.status == StatusAnimal.RESERVADO
    assert svc.rodar_expiracao(T0 + timedelta(hours=49)) == [rex]
    assert rex.status == StatusAnimal.DISPONIVEL


def test_expiracao_notifica_proximo_da_fila():
    svc, rex, ana, bia = cenario()
    msgs = []
    svc.inscrever(msgs.append)
    svc.reservar(ana, rex, T0)
    svc.entrar_na_fila(bia, rex, T0)
    svc.rodar_expiracao(T0 + timedelta(hours=50))
    assert len(msgs) == 1 and "Bia" in msgs[0]


def test_adotar_sem_reserva_falha():
    svc, rex, ana, _ = cenario()
    with pytest.raises(ReservaInvalidaError):
        svc.adotar(ana, rex, T0)


def test_adotar_com_reserva_gera_contrato():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    contrato = svc.adotar(ana, rex, T0 + timedelta(hours=1))
    assert "Ana" in contrato and "Rex" in contrato and "R$" in contrato
    assert rex.status == StatusAnimal.ADOTADO and rex in ana.animais_adotados


def test_adotar_apos_expirar_falha():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    with pytest.raises(ReservaInvalidaError):
        svc.adotar(ana, rex, T0 + timedelta(hours=60))


def test_devolucao_com_problema_vai_para_quarentena():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    svc.adotar(ana, rex, T0)
    svc.devolver(rex, "agressivo", problema_saude=True, agora=T0)
    assert rex.status == StatusAnimal.QUARENTENA and rex not in ana.animais_adotados


def test_devolucao_simples_e_relatorio_por_motivo():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    svc.adotar(ana, rex, T0)
    svc.devolver(rex, "mudança de cidade", agora=T0)
    assert rex.status == StatusAnimal.DEVOLVIDO
    assert devolucoes_por_motivo([rex]) == {"mudança de cidade": 1}


def test_reavaliar_quarentena_para_disponivel():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    svc.adotar(ana, rex, T0)
    svc.devolver(rex, "doente", problema_saude=True, agora=T0)
    svc.reavaliar(rex, StatusAnimal.DISPONIVEL)
    assert rex.status == StatusAnimal.DISPONIVEL


def test_fila_prioriza_pontuacao_e_depois_tempo():
    _, _, ana, bia = cenario()
    fila = FilaEspera()
    fila.adicionar(bia, 50.0, T0)
    fila.adicionar(ana, 90.0, T0 + timedelta(hours=1))
    assert len(fila) == 2
    assert fila.proximo().adotante == ana


def test_compatibilidade_entre_0_e_100_e_criancas_reduzem():
    _, rex, ana, bia = cenario(temperamento=("arisco",))
    pesos = Settings().pesos
    assert 0 <= calcular_compatibilidade(ana, rex, pesos) <= 100
    assert calcular_compatibilidade(bia, rex, pesos) < calcular_compatibilidade(ana, rex, pesos)


def test_estrategias_de_taxa():
    _, rex, _, _ = cenario()
    base = BaseFeeStrategy().calcular(rex)
    assert SeniorFee().calcular(rex) < base < PuppyFee().calcular(rex)


def test_taxa_de_adocao_por_porte():
    svc, rex, ana, _ = cenario()
    svc.reservar(ana, rex, T0)
    svc.adotar(ana, rex, T0)
    assert taxa_adocao_por([rex], lambda a: a.porte) == {"M": 1.0}
