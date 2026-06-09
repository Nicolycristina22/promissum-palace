from abc import ABC, abstractmethod
class ServicoReserva(ABC):

    @abstractmethod
    def get_descricao(self) -> str:
        pass

    @abstractmethod
    def custo(self) -> float:
        pass
