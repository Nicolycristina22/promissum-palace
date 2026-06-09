from datetime import date
from dominio.reserva import Reserva, StatusReserva


class ReservaFactory:

    @staticmethod
    def criar_reserva(hospede, quarto, check_in, check_out,
                      observacao="", forma_pagamento="PIX"):

        if not hospede:
            raise ValueError("Hóspede inválido")
        if not quarto:
            raise ValueError("Quarto inválido")
        if not check_in or not check_out:
            raise ValueError("Datas inválidas")
        if check_out <= check_in:
            raise ValueError("Check-out deve ser após check-in")

        delta = (check_out - check_in).days
        total_diarias = delta
        valor_total   = round(total_diarias * quarto.preco, 2)

        return Reserva._criar(
            None,
            hospede,
            quarto,
            check_in,
            check_out,
            StatusReserva.ATIVO,
            total_diarias,
            valor_total,
            observacao,
            forma_pagamento
        )
