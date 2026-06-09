from decorator.servico_decorator import ServicoDecorator
class CafeDaManha(ServicoDecorator):

    def get_descricao(self) -> str:
        return self._servico.get_descricao() + ", Café da manhã"

    def custo(self) -> float:
        return self._servico.custo() + 50.0
class Estacionamento(ServicoDecorator):

    def get_descricao(self) -> str:
        return self._servico.get_descricao() + ", Estacionamento"

    def custo(self) -> float:
        return self._servico.custo() + 30.0
class LateCheckout(ServicoDecorator):

    def get_descricao(self) -> str:
        return self._servico.get_descricao() + ", Late check-out"

    def custo(self) -> float:
        return self._servico.custo() + 80.0
class TransferAeroporto(ServicoDecorator):

    def get_descricao(self) -> str:
        return self._servico.get_descricao() + ", Transfer aeroporto"

    def custo(self) -> float:
        return self._servico.custo() + 120.0
