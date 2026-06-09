from enum import Enum


class TipoQuarto(Enum):
    STANDARD = "Standard"
    LUXO     = "Luxo"
    SUITE    = "Suíte"


class Quarto:

    def __init__(self, *args, **kwargs):
        raise Exception("Use QuartoCommand para criar o quarto")

    @classmethod
    def _criar(cls, quarto_id, numero, tipo_quarto, preco, capacidade, descricao, andar, tem_varanda, tem_banheira, area_m2, amenidades):
        obj = cls.__new__(cls)
        obj._id          = quarto_id
        obj._numero      = numero
        obj._tipo_quarto = tipo_quarto
        obj._preco       = preco
        obj._capacidade  = capacidade
        obj._descricao   = descricao
        obj._andar       = andar
        obj._tem_varanda  = tem_varanda
        obj._tem_banheira = tem_banheira
        obj._area_m2     = area_m2
        obj._amenidades  = amenidades
        return obj

    def __str__(self):
        return (f"Tipo: {self._tipo_quarto.value}, Número: {self._numero}, "
                f"Preço: R${self._preco:.2f}, Andar: {self._andar}, "
                f"Área: {self._area_m2}m², Capacidade: {self._capacidade} pessoa(s)")

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        if self._id is not None:
            raise ValueError("ID já definido, não pode ser alterado")
        self._id = value

    @property
    def numero(self):
        return self._numero

    @property
    def tipo_quarto(self):
        return self._tipo_quarto

    @property
    def preco(self):
        return self._preco

    @property
    def capacidade(self):
        return self._capacidade

    @property
    def descricao(self):
        return self._descricao

    @property
    def andar(self):
        return self._andar

    @property
    def tem_varanda(self):
        return self._tem_varanda

    @property
    def tem_banheira(self):
        return self._tem_banheira

    @property
    def area_m2(self):
        return self._area_m2

    @property
    def amenidades(self):
        return self._amenidades


    def atualizar_preco(self, novo_preco: float):
        if novo_preco <= 0:
            raise ValueError("O preço deve ser maior que 0")
        self._preco = novo_preco

    def atualizar_descricao(self, nova_descricao: str):
        if not nova_descricao or len(nova_descricao.strip()) < 3:
            raise ValueError("Descrição inválida")
        self._descricao = nova_descricao.strip()
