from datetime import date, datetime
from dominio.reserva import Reserva, StatusReserva


class ReservaBuilder:

    def __init__(self):
        self._hospede        = None
        self._quarto         = None
        self._check_in       = None
        self._check_out      = None
        self._status         = None
        self._total_diarias  = None
        self._valor_total    = None
        self._observacao     = ""
        self._forma_pagamento = "PIX"

    def set_hospede(self, hospede):
        self._hospede = hospede
        return self

    def set_quarto(self, quarto):
        self._quarto = quarto
        return self

    def set_check_in(self, check_in):
        self._check_in = self._to_date(check_in)
        return self

    def set_check_out(self, check_out):
        self._check_out = self._to_date(check_out)
        return self

    def set_status(self, status):
        if isinstance(status, str):
            self._status = StatusReserva(status)
        else:
            self._status = status
        return self

    def set_total_diarias(self, total_diarias):
        self._total_diarias = int(total_diarias) if total_diarias is not None else None
        return self

    def set_valor_total(self, valor_total):
        self._valor_total = float(valor_total) if valor_total is not None else None
        return self

    def set_observacao(self, observacao):
        self._observacao = observacao or ""
        return self

    def set_forma_pagamento(self, forma_pagamento):
        self._forma_pagamento = forma_pagamento or "PIX"
        return self

    def build(self):
        if not self._hospede:
            raise ValueError("Hóspede obrigatório")
        if not self._quarto:
            raise ValueError("Quarto obrigatório")
        if not self._check_in or not self._check_out:
            raise ValueError("Datas obrigatórias")
        if self._status is None:
            raise ValueError("Status obrigatório")

        if self._total_diarias is None:
            self._total_diarias = (self._check_out - self._check_in).days
        if self._valor_total is None:
            self._valor_total = round(self._total_diarias * self._quarto.preco, 2)

        return Reserva._criar(
            None,
            self._hospede,
            self._quarto,
            self._check_in,
            self._check_out,
            self._status,
            self._total_diarias,
            self._valor_total,
            self._observacao,
            self._forma_pagamento
        )

    @staticmethod
    def _to_date(value):
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value
