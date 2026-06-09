from decorator.servico_reserva_interface import ServicoReserva
class ReservaBasica(ServicoReserva):

    def __init__(self, reserva):
        self._reserva = reserva

    def get_descricao(self) -> str:
        return (f"Quarto {self._reserva.quarto.numero} "
                f"({self._reserva.total_diarias} diária(s))")

    def custo(self) -> float:
        return float(self._reserva.quarto.preco * self._reserva.total_diarias)
