from abc import ABC, abstractmethod


class HospedeRepositorioInterface(ABC):


    @abstractmethod
    def salvar(self, hospede):
        pass

    @abstractmethod
    def encontrar_por_id(self, hospede_id):
        pass

    @abstractmethod
    def deletar(self, hospede_id):
        pass

    @abstractmethod
    def listar(self):
        pass
