from abc import ABC, abstractmethod


class QuartoCommand(ABC):
    

    @abstractmethod
    def executar(self, numero, tipo_quarto, preco):
        pass