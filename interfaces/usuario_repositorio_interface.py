from abc import ABC, abstractmethod


class UsuarioRepositorioInterface(ABC):

    @abstractmethod
    def encontrar_por_email(self, email: str):
        pass

    @abstractmethod
    def encontrar_por_id(self, usuario_id: int):
        pass

    @abstractmethod
    def salvar(self, usuario):
        pass
