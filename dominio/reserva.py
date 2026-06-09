from datetime import date
from enum import Enum


class StatusReserva(Enum):
    ATIVO     = "Ativo"
    CANCELADO = "Cancelado"


class Reserva:

    def __init__(self, *args, **kwargs):
        raise Exception("Use ReservaFactory para criar a reserva")

    @classmethod
    def _criar(cls, reserva_id, hospede, quarto, check_in: date, check_out: date,
               status, total_diarias, valor_total, observacao, forma_pagamento):
        obj = cls.__new__(cls)
        obj._id              = reserva_id
        obj._hospede         = hospede
        obj._quarto          = quarto
        obj._check_in        = check_in
        obj._check_out       = check_out
        obj._status          = status
        obj._total_diarias   = total_diarias
        obj._valor_total     = valor_total
        obj._observacao      = observacao
        obj._forma_pagamento = forma_pagamento
        return obj

    def __str__(self):
        return (f"Hóspede: {self._hospede.nome}, Quarto: {self._quarto.numero}, "
                f"Check-in: {self._check_in}, Check-out: {self._check_out}, "
                f"Status: {self._status.value}, Total: R${self._valor_total:.2f}")


    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if self._id is not None:
            raise ValueError("ID já definido, não pode ser alterado")
        self._id = value

    @property
    def hospede(self):
        return self._hospede

    @property
    def quarto(self):
        return self._quarto

    @property
    def check_in(self):
        return self._check_in

    @property
    def check_out(self):
        return self._check_out

    @property
    def status(self):
        return self._status

    @property
    def total_diarias(self):
        return self._total_diarias

    @property
    def valor_total(self):
        return self._valor_total

    @property
    def observacao(self):
        return self._observacao

    @property
    def forma_pagamento(self):
        return self._forma_pagamento


    def cancelar(self):
        if self._status == StatusReserva.CANCELADO:
            raise ValueError("Reserva já está cancelada")
        self._status = StatusReserva.CANCELADO

    def atualizar_observacao(self, nova_obs: str):
        self._observacao = nova_obs.strip()

    def atualizar_totais(self, total_diarias: int, valor_total: float):
        if total_diarias is not None:
            self._total_diarias = total_diarias
        if valor_total is not None:
            self._valor_total = valor_total

    def set_servicos_extras(self, servicos: list):
            self._servicos_extras = servicos or []

    @property
    def servicos_extras(self) -> list:
        return getattr(self, "_servicos_extras", [])
