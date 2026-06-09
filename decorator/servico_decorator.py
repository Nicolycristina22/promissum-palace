from decorator.servico_reserva_interface import ServicoReserva
class ServicoDecorator(ServicoReserva):

    def __init__(self, servico: ServicoReserva):
        self._servico = servico

    def get_descricao(self) -> str:
        return self._servico.get_descricao()

    def custo(self) -> float:
        return self._servico.custo()
