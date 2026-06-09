from abc import ABC, abstractmethod


class QuartoRepositorioInterface(ABC):


    @abstractmethod
    def salvar(self, quarto):
        pass

    @abstractmethod
    def encontrar_por_id(self, quarto_id):
        pass

    @abstractmethod
    def encontrar_todos(self):
        pass

    @abstractmethod
    def deletar(self, quarto_id):
        pass

    @abstractmethod
    def listar(self):
        pass
