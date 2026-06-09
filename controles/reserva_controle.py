from factory.reserva_factory import ReservaFactory


class ReservaControle:
    def __init__(self, repositorio, servico, hospede_repo, quarto_repo):
        self._repositorio  = repositorio
        self._servico      = servico
        self._hospede_repo = hospede_repo
        self._quarto_repo  = quarto_repo

    def criar_reserva(self, hospede_id, quarto_id, check_in, check_out,
                      observacao="", forma_pagamento="PIX"):
        hospede = self._hospede_repo.encontrar_por_id(hospede_id)
        quarto  = self._quarto_repo.encontrar_por_id(quarto_id)

        if not hospede:
            raise Exception("Hóspede não encontrado")
        if not quarto:
            raise Exception("Quarto não encontrado")

        reserva = ReservaFactory.criar_reserva(
            hospede, quarto, check_in, check_out, observacao, forma_pagamento
        )
        self._servico.criar_reserva(reserva)
        return reserva

    def buscar_por_id(self, reserva_id):
        reserva = self._repositorio.encontrar_por_id(reserva_id)
        if not reserva:
            raise Exception("Reserva não encontrada")
        return reserva

    def listar_reservas_por_hospede(self, hospede_id):
        return self._repositorio.encontrar_por_hospede(hospede_id)

    def listar_reservas(self):
        return self._repositorio.listar()

    def atualizar_reserva(self, reserva_id, quarto_id=None, check_in=None,
                          check_out=None, total_diarias=None, valor_total=None):
        reserva = self._repositorio.encontrar_por_id(reserva_id)
        if not reserva:
            raise Exception("Reserva não encontrada")

        if quarto_id is not None:
            quarto = self._quarto_repo.encontrar_por_id(quarto_id)
            if not quarto:
                raise Exception("Quarto não encontrado")
            reserva._quarto = quarto

        if check_in is not None:
            reserva._check_in = check_in
        if check_out is not None:
            reserva._check_out = check_out
        if total_diarias is not None:
            reserva._total_diarias = total_diarias
        if valor_total is not None:
            reserva._valor_total = valor_total

        self._repositorio.salvar(reserva)
        return reserva

    def cancelar_reserva(self, reserva_id):
        self._servico.cancelar_reserva(reserva_id)

    def deletar_reserva(self, reserva_id):
        reserva = self._repositorio.encontrar_por_id(reserva_id)
        if not reserva:
            raise Exception("Reserva não encontrada")
        self._repositorio.deletar(reserva_id)
