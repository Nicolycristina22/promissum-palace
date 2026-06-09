from abc import ABC, abstractmethod


class ReservaRepositorioInterface(ABC):

    @abstractmethod
    def salvar(self, reserva):
        pass

    @abstractmethod
    def encontrar_por_id(self, reserva_id):
        pass

    @abstractmethod
    def encontrar_todos(self):
        pass

    @abstractmethod
    def encontrar_por_quarto(self, quarto_id):
        pass

    @abstractmethod
    def encontrar_por_hospede(self, hospede_id):
        pass

    @abstractmethod
    def deletar(self, reserva_id):
        pass

    @abstractmethod
    def listar(self):
        pass
