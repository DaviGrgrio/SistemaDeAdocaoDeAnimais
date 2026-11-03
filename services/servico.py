from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional

from models.adotante import Adotante
from models.animal import Animal, StatusAnimal
from services.config import Settings
from models.excecoes import ReservaInvalidaError, TransicaoDeEstadoInvalidaError
from services.fila import FilaEspera
from services.politicas import validar_politica
from services.taxas import escolher_estrategia
from services.compatibilidade import calcular_compatibilidade


@dataclass
class Reserva:
    animal: Animal
    adotante: Adotante
    criada_em: datetime
    expira_em: datetime

    def expirada(self, agora: datetime) -> bool:
        return agora >= self.expira_em


class AdocaoService:
    """Regras de negócio: reserva, adoção, fila, devolução e reavaliação."""

    def __init__(self, settings: Settings, animais: Optional[List[Animal]] = None,
                 adotantes: Optional[List[Adotante]] = None) -> None:
        self.settings = settings
        self.animais: Dict[int, Animal] = {a.id_animal: a for a in animais or []}
        self.adotantes: Dict[int, Adotante] = {a.id_adotante: a for a in adotantes or []}
        self._reservas: Dict[int, Reserva] = {}
        self._filas: Dict[int, FilaEspera] = {}
        self._observadores: List[Callable[[str], None]] = []

    # --- Observer ---
    def inscrever(self, observador: Callable[[str], None]) -> None:
        self._observadores.append(observador)

    def _notificar(self, mensagem: str) -> None:
        for obs in self._observadores:
            obs(mensagem)

    # --- Reserva / fila ---
    def reservar(self, adotante: Adotante, animal: Animal,
                 agora: Optional[datetime] = None) -> Reserva:
        agora = agora or datetime.now()
        if animal.id_animal in self._reservas:
            raise ReservaInvalidaError("O animal já possui uma reserva ativa.")
        if animal.status != StatusAnimal.DISPONIVEL:
            raise ReservaInvalidaError(f"Animal {animal.status.value}: não pode ser reservado.")
        validar_politica(adotante, animal, self.settings)
        animal.alterar_status(StatusAnimal.RESERVADO, quando=agora)
        reserva = Reserva(animal, adotante, agora,
                          agora + timedelta(hours=self.settings.reserva_horas))
        self._reservas[animal.id_animal] = reserva
        return reserva

    def entrar_na_fila(self, adotante: Adotante, animal: Animal,
                       agora: Optional[datetime] = None) -> int:
        """Entra na fila do animal e devolve o tamanho da fila."""
        validar_politica(adotante, animal, self.settings)
        pontuacao = calcular_compatibilidade(adotante, animal, self.settings.pesos)
        fila = self._filas.setdefault(animal.id_animal, FilaEspera())
        fila.adicionar(adotante, pontuacao, agora)
        return len(fila)

    def rodar_expiracao(self, agora: Optional[datetime] = None) -> List[Animal]:
        """Expira reservas vencidas, libera os animais e notifica o próximo da fila."""
        agora = agora or datetime.now()
        liberados: List[Animal] = []
        for id_animal, reserva in list(self._reservas.items()):
            if not reserva.expirada(agora):
                continue
            del self._reservas[id_animal]
            animal = reserva.animal
            animal.alterar_status(StatusAnimal.DISPONIVEL, "reserva expirada", agora)
            liberados.append(animal)
            fila = self._filas.get(id_animal)
            proximo = fila.proximo() if fila else None
            if proximo:
                msg = f"{proximo.adotante.nome} é o próximo da fila para {animal.nome}."
                animal.registrar_evento("notificacao_fila", msg, agora)
                self._notificar(msg)
        return liberados

    # --- Adoção / devolução / reavaliação ---
    def adotar(self, adotante: Adotante, animal: Animal,
               agora: Optional[datetime] = None) -> str:
        """Conclui a adoção (exige reserva ativa) e devolve o texto do contrato."""
        agora = agora or datetime.now()
        reserva = self._reservas.get(animal.id_animal)
        if reserva is None or reserva.adotante != adotante:
            raise ReservaInvalidaError("É preciso ter uma reserva ativa em nome do adotante.")
        if reserva.expirada(agora):
            raise ReservaInvalidaError("A reserva expirou.")
        taxa = escolher_estrategia(animal, self.settings.taxa_padrao).calcular(animal)
        animal.alterar_status(StatusAnimal.ADOTADO, quando=agora)
        animal.registrar_evento("adocao", f"adotante={adotante.nome}; taxa={taxa:.2f}", agora)
        adotante.vincular_animal(animal)
        del self._reservas[animal.id_animal]
        self._filas.pop(animal.id_animal, None)
        return (f"CONTRATO DE ADOÇÃO - {agora:%d/%m/%Y}\n\nAnimal: {animal}\nAdotante: {adotante}\n"
                f"Taxa: R$ {taxa:.2f}\n\nTermos: o adotante se compromete a oferecer cuidados "
                "adequados, manter a vacinação em dia e devolver o animal ao abrigo caso não "
                "possa mantê-lo.")

    def devolver(self, animal: Animal, motivo: str, problema_saude: bool = False,
                 agora: Optional[datetime] = None) -> None:
        """Registra a devolução; com problema de saúde/comportamento, vai para QUARENTENA."""
        agora = agora or datetime.now()
        animal.alterar_status(StatusAnimal.DEVOLVIDO, quando=agora)
        animal.registrar_evento("devolucao", motivo, agora)
        if animal.adotante is not None:
            animal.adotante.desvincular_animal(animal)
        if problema_saude:
            animal.alterar_status(StatusAnimal.QUARENTENA,
                                  "problema de saúde/comportamento", agora)

    def reavaliar(self, animal: Animal, novo_status: StatusAnimal,
                  agora: Optional[datetime] = None) -> None:
        """Reavaliação: leva o animal a DISPONIVEL ou INADOTAVEL."""
        if novo_status not in (StatusAnimal.DISPONIVEL, StatusAnimal.INADOTAVEL):
            raise TransicaoDeEstadoInvalidaError(
                "A reavaliação só leva a DISPONIVEL ou INADOTAVEL.")
        animal.alterar_status(novo_status, "reavaliação", agora)

    def remover_animal(self, animal: Animal) -> None:
        if animal.status in (StatusAnimal.RESERVADO, StatusAnimal.ADOTADO):
            raise ValueError("Não é possível excluir um animal reservado ou adotado.")
        del self.animais[animal.id_animal]
        self._filas.pop(animal.id_animal, None)

    # --- Estado (reservas e filas) para persistência entre comandos da CLI ---
    def exportar_estado(self) -> dict:
        return {
            "reservas": [
                {"animal_id": r.animal.id_animal, "adotante_id": r.adotante.id_adotante,
                 "criada_em": r.criada_em.isoformat(), "expira_em": r.expira_em.isoformat()}
                for r in self._reservas.values()
            ],
            "filas": {
                str(id_animal): [
                    {"adotante_id": e.adotante.id_adotante, "pontuacao": e.pontuacao,
                     "entrada_em": e.entrada_em.isoformat()}
                    for e in fila.entradas
                ]
                for id_animal, fila in self._filas.items()
            },
        }

    def importar_estado(self, dados: dict) -> None:
        for r in dados.get("reservas", []):
            animal = self.animais[r["animal_id"]]
            self._reservas[animal.id_animal] = Reserva(
                animal, self.adotantes[r["adotante_id"]],
                datetime.fromisoformat(r["criada_em"]),
                datetime.fromisoformat(r["expira_em"]))
        for id_animal, entradas in dados.get("filas", {}).items():
            fila = self._filas.setdefault(int(id_animal), FilaEspera())
            for e in entradas:
                fila.adicionar(self.adotantes[e["adotante_id"]], e["pontuacao"],
                               datetime.fromisoformat(e["entrada_em"]))
