"""Interface de linha de comando (subcomandos) do sistema de adoção."""

import argparse
import sys
from typing import List, Optional

from models.adotante import Adotante
from models.animal import SexoAnimal, StatusAnimal
from models.cachorro import Cachorro
from services.config import Settings
from models.excecoes import (PoliticaNaoAtendidaError, RepositorioError,
                             ReservaInvalidaError, TransicaoDeEstadoInvalidaError)
from models.gato import Gato
from services.servico import AdocaoService
from repositories.repositorio_json import RepositorioJSON
from services.relatorios import (devolucoes_por_motivo, relatorio_disponiveis_adotados,
                            taxa_adocao_por, tempo_medio_adocao_dias, top_adotaveis)


def _animal(svc, id_animal: int):
    if id_animal not in svc.animais:
        raise ValueError(f"Animal {id_animal} não encontrado.")
    return svc.animais[id_animal]


def _adotante(svc, id_adotante: int):
    if id_adotante not in svc.adotantes:
        raise ValueError(f"Adotante {id_adotante} não encontrado.")
    return svc.adotantes[id_adotante]


# ---------------- comandos ----------------
def cmd_cadastrar_animal(svc, a) -> None:
    base = dict(
        id_animal=max(svc.animais, default=0) + 1, nome=a.nome, sexo=SexoAnimal[a.sexo],
        idade_meses=a.idade_meses, porte=a.porte,
        temperamento=[t.strip() for t in a.temperamento.split(",") if t.strip()],
    )
    if a.tipo == "cachorro":
        if not a.raca or not a.passeio:
            raise ValueError("Cachorro exige --raca e --passeio.")
        animal = Cachorro(**base, raca=a.raca, necessidade_passeio=a.passeio)
    else:
        if a.independencia is None:
            raise ValueError("Gato exige --independencia (1 a 5).")
        animal = Gato(**base, nivel_independencia=a.independencia,
                      fiv_felv_negativo=not a.fiv_felv_positivo,
                      usa_caixa_areia=not a.sem_caixa_areia)
    svc.animais[animal.id_animal] = animal
    print(f"Animal cadastrado com ID {animal.id_animal}: {animal}")


def cmd_cadastrar_adotante(svc, a) -> None:
    adotante = Adotante(max(svc.adotantes, default=0) + 1, a.nome, a.idade, a.moradia, a.area,
                        a.experiencia, a.criancas, a.outros_animais)
    svc.adotantes[adotante.id_adotante] = adotante
    print(f"Adotante cadastrado com ID {adotante.id_adotante}: {adotante}")


def cmd_atualizar_animal(svc, a) -> None:
    animal = _animal(svc, a.id)
    if a.nome:
        animal.nome = a.nome
    if a.idade_meses is not None:
        animal.idade_meses = a.idade_meses
    if a.porte:
        animal.porte = a.porte
    print(f"Animal atualizado: {animal}")


def cmd_excluir_animal(svc, a) -> None:
    svc.remover_animal(_animal(svc, a.id))
    print(f"Animal {a.id} excluído.")


def cmd_listar(svc, a) -> None:
    animais = sorted(svc.animais.values(), key=lambda x: x.id_animal)
    if a.status:
        animais = [x for x in animais if x.status.name == a.status]
    print("ANIMAIS")
    for x in animais:
        print(f"  [{x.id_animal}] {x}")
    print("ADOTANTES")
    for ad in svc.adotantes.values():
        print(f"  [{ad.id_adotante}] {ad}")


def cmd_reservar(svc, a) -> None:
    reserva = svc.reservar(_adotante(svc, a.adotante), _animal(svc, a.animal))
    print(f"Reserva criada. Expira em {reserva.expira_em:%d/%m/%Y %H:%M}.")


def cmd_fila(svc, a) -> None:
    posicao = svc.entrar_na_fila(_adotante(svc, a.adotante), _animal(svc, a.animal))
    print(f"Adotante na fila de espera (tamanho da fila: {posicao}).")


def cmd_adotar(svc, a) -> None:
    print(svc.adotar(_adotante(svc, a.adotante), _animal(svc, a.animal)))


def cmd_devolver(svc, a) -> None:
    animal = _animal(svc, a.animal)
    svc.devolver(animal, a.motivo, a.problema_saude)
    print(f"Devolução registrada. Status atual: {animal.status.value}.")


def cmd_reavaliar(svc, a) -> None:
    animal = _animal(svc, a.animal)
    svc.reavaliar(animal, StatusAnimal[a.status])
    print(f"Animal reavaliado. Status atual: {animal.status.value}.")


def cmd_rodar_expiracao(svc, a) -> None:
    liberados = svc.rodar_expiracao()
    if liberados:
        print("Reservas expiradas, animais liberados:", ", ".join(x.nome for x in liberados))
    else:
        print("Nenhuma reserva expirada.")


def cmd_relatorio(svc, a) -> None:
    animais, adotantes = list(svc.animais.values()), list(svc.adotantes.values())
    if a.tipo == "disponiveis":
        print(relatorio_disponiveis_adotados(animais))
    elif a.tipo == "top":
        linhas = top_adotaveis(animais, adotantes, svc.settings.pesos)
        if not linhas:
            print("Cadastre adotantes para calcular a compatibilidade.")
        for pos, (animal, media) in enumerate(linhas, 1):
            print(f"{pos}. {animal.nome} - compatibilidade média {media}")
    elif a.tipo == "taxas":
        for titulo, chave in (("espécie", lambda x: type(x).__name__),
                              ("porte", lambda x: x.porte)):
            print(f"Taxa de adoção por {titulo}:")
            for k, v in taxa_adocao_por(animais, chave).items():
                print(f"  {k}: {v:.0%}")
    elif a.tipo == "tempo":
        media = tempo_medio_adocao_dias(animais)
        print("Nenhuma adoção registrada." if media is None
              else f"Tempo médio até a adoção: {media:.1f} dias")
    else:  # devolucoes
        motivos = devolucoes_por_motivo(animais)
        print("Devoluções por motivo:" if motivos else "Nenhuma devolução registrada.")
        for motivo, n in motivos.items():
            print(f"  {motivo}: {n}")


def cmd_seed(svc, a) -> None:
    from seed import popular
    popular(a.dados)
    print("Dados de exemplo criados.")


# ---------------- parser ----------------
def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="adocao", description="Sistema de Adoção de Animais")
    p.add_argument("--dados", default="data", help="pasta dos arquivos JSON (padrão: data)")
    p.add_argument("--settings", default="settings.json", help="arquivo de configurações")
    sub = p.add_subparsers(dest="comando", required=True)

    def novo(nome, func, muta, ajuda):
        sp = sub.add_parser(nome, help=ajuda)
        sp.set_defaults(func=func, muta=muta)
        return sp

    sp = novo("cadastrar-animal", cmd_cadastrar_animal, True, "cadastra cachorro ou gato")
    sp.add_argument("--tipo", required=True, choices=["cachorro", "gato"], type=str.lower)
    sp.add_argument("--nome", required=True)
    sp.add_argument("--sexo", required=True, choices=["MACHO", "FEMEA"], type=str.upper)
    sp.add_argument("--idade-meses", required=True, type=int)
    sp.add_argument("--porte", required=True, choices=["P", "M", "G"], type=str.upper)
    sp.add_argument("--temperamento", default="", help="separado por vírgula")
    sp.add_argument("--raca", help="(cachorro)")
    sp.add_argument("--passeio", help="(cachorro) necessidade de passeio: baixa/media/alta")
    sp.add_argument("--independencia", type=int, help="(gato) nível de 1 a 5")
    sp.add_argument("--fiv-felv-positivo", action="store_true", help="(gato)")
    sp.add_argument("--sem-caixa-areia", action="store_true", help="(gato)")

    sp = novo("cadastrar-adotante", cmd_cadastrar_adotante, True, "cadastra adotante")
    sp.add_argument("--nome", required=True)
    sp.add_argument("--idade", required=True, type=int)
    sp.add_argument("--moradia", required=True, choices=["casa", "apto", "sítio"],
                    type=str.lower)
    sp.add_argument("--area", required=True, type=float, help="área útil em m²")
    sp.add_argument("--experiencia", action="store_true", help="tem experiência com pets")
    sp.add_argument("--criancas", action="store_true", help="há crianças em casa")
    sp.add_argument("--outros-animais", action="store_true")

    sp = novo("atualizar-animal", cmd_atualizar_animal, True, "atualiza nome, idade ou porte")
    sp.add_argument("--id", required=True, type=int)
    sp.add_argument("--nome")
    sp.add_argument("--idade-meses", type=int)
    sp.add_argument("--porte", choices=["P", "M", "G"], type=str.upper)

    sp = novo("excluir-animal", cmd_excluir_animal, True, "exclui animal")
    sp.add_argument("--id", required=True, type=int)

    sp = novo("listar", cmd_listar, False, "lista animais e adotantes")
    sp.add_argument("--status", choices=[s.name for s in StatusAnimal], type=str.upper)

    for nome, func, ajuda in (("reservar", cmd_reservar, "reserva um animal"),
                              ("fila", cmd_fila, "entra na fila de espera"),
                              ("adotar", cmd_adotar, "conclui a adoção (exige reserva)")):
        sp = novo(nome, func, True, ajuda)
        sp.add_argument("--animal", required=True, type=int)
        sp.add_argument("--adotante", required=True, type=int)

    sp = novo("devolver", cmd_devolver, True, "registra devolução")
    sp.add_argument("--animal", required=True, type=int)
    sp.add_argument("--motivo", required=True)
    sp.add_argument("--problema-saude", action="store_true",
                    help="envia o animal para QUARENTENA")

    sp = novo("reavaliar", cmd_reavaliar, True, "reavalia animal em quarentena/devolvido")
    sp.add_argument("--animal", required=True, type=int)
    sp.add_argument("--status", required=True, choices=["DISPONIVEL", "INADOTAVEL"],
                    type=str.upper)

    novo("rodar-expiracao", cmd_rodar_expiracao, True, "expira reservas vencidas")

    sp = novo("relatorio", cmd_relatorio, False, "gera relatórios")
    sp.add_argument("tipo", choices=["disponiveis", "top", "taxas", "tempo", "devolucoes"])

    novo("seed", cmd_seed, False, "cria dados de exemplo")
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = construir_parser().parse_args(argv)
    repo = RepositorioJSON(args.dados)
    try:
        animais, adotantes = repo.carregar()
        svc = AdocaoService(Settings.carregar(args.settings), animais, adotantes)
        svc.importar_estado(repo.carregar_estado())
        svc.inscrever(lambda msg: print(f"[NOTIFICAÇÃO] {msg}"))
        args.func(svc, args)
        if args.muta:  # só grava se o comando deu certo
            repo.salvar(list(svc.animais.values()), list(svc.adotantes.values()))
            repo.salvar_estado(svc.exportar_estado())
    except (ReservaInvalidaError, PoliticaNaoAtendidaError, TransicaoDeEstadoInvalidaError,
            RepositorioError, ValueError) as e:
        print(f"Erro: {e}", file=sys.stderr)
        return 1
    return 0
