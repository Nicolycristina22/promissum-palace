from dominio.quarto import Quarto, TipoQuarto


class QuartoBuilder:

    def __init__(self):
        self._numero       = None
        self._tipo_quarto  = None
        self._preco        = None
        self._capacidade   = None
        self._descricao    = ""
        self._andar        = 1
        self._tem_varanda  = False
        self._tem_banheira = False
        self._area_m2      = 0.0
        self._amenidades   = ""

    def set_numero(self, numero):
        self._numero = int(numero)
        return self

    def set_tipo_quarto(self, tipo):
        if isinstance(tipo, str):
            self._tipo_quarto = TipoQuarto[tipo.upper()]
        else:
            self._tipo_quarto = tipo
        return self

    def set_preco(self, preco):
        self._preco = float(preco)
        return self

    def set_capacidade(self, capacidade):
        self._capacidade = int(capacidade)
        return self

    def set_descricao(self, descricao):
        self._descricao = descricao or ""
        return self

    def set_andar(self, andar):
        self._andar = int(andar)
        return self

    def set_tem_varanda(self, tem_varanda):
        self._tem_varanda = bool(tem_varanda)
        return self

    def set_tem_banheira(self, tem_banheira):
        self._tem_banheira = bool(tem_banheira)
        return self

    def set_area_m2(self, area_m2):
        self._area_m2 = float(area_m2)
        return self

    def set_amenidades(self, amenidades):
        self._amenidades = amenidades or ""
        return self

    def build(self):
        if not self._numero:
            raise ValueError("Número do quarto obrigatório")
        if not self._tipo_quarto:
            raise ValueError("Tipo do quarto obrigatório")
        if self._preco is None or self._preco <= 0:
            raise ValueError("Preço inválido")

        return Quarto._criar(
            None,
            self._numero,
            self._tipo_quarto,
            self._preco,
            self._capacidade,
            self._descricao,
            self._andar,
            self._tem_varanda,
            self._tem_banheira,
            self._area_m2,
            self._amenidades
        )
