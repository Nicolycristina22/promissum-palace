from datetime import datetime, date
from dominio.reserva import StatusReserva


class ReservaServico:


    def __init__(self, hospede_repositorio, quarto_repositorio, reserva_repositorio):
        self._hospede_repositorio = hospede_repositorio
        self._quarto_repositorio  = quarto_repositorio
        self._reserva_repositorio = reserva_repositorio

    def criar_reserva(self, reserva):
        
        hospede = reserva.hospede
        quarto  = reserva.quarto

        if not self._hospede_repositorio.encontrar_por_id(hospede.id):
            raise Exception("Hóspede não encontrado")

        if not self._quarto_repositorio.encontrar_por_id(quarto.id):
            raise Exception("Quarto não encontrado")

        check_in  = self._to_date(reserva.check_in)
        check_out = self._to_date(reserva.check_out)

        if not self.checar_quarto_disponibilidade(quarto.id, check_in, check_out):
            raise Exception("Quarto já reservado nesse período")

        self._reserva_repositorio.salvar(reserva)

    def checar_quarto_disponibilidade(self, quarto_id, check_in, check_out):
        reservas = self._reserva_repositorio.encontrar_por_quarto(quarto_id)

        for reserva in reservas:
            
            if reserva.status == StatusReserva.CANCELADO:
                continue

            ci_ex = self._to_date(reserva.check_in)
            co_ex = self._to_date(reserva.check_out)

            if (check_in < co_ex) and (check_out > ci_ex):
                return False

        return True

    def cancelar_reserva(self, reserva_id):
        reserva = self._reserva_repositorio.encontrar_por_id(reserva_id)
        if not reserva:
            raise Exception("Reserva não encontrada")
        reserva.cancelar()
        self._reserva_repositorio.salvar(reserva)

    def listar_reservas(self):
        return self._reserva_repositorio.listar()

    @staticmethod
    def _to_date(value):
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        return value
