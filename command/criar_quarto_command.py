from command.quarto_command import QuartoCommand
from dominio.quarto import Quarto, TipoQuarto


class CriarQuartoCommand(QuartoCommand):

    

    def __init__(self, quarto_repo):
        self._quarto_repo = quarto_repo

    def executar(self, numero, tipo_quarto, preco, capacidade=2, descricao="", andar=1, tem_varanda=False, tem_banheira=False, area_m2=20.0, amenidades=""):

        
        if not numero:
            raise ValueError("Número do quarto inválido")

        if not tipo_quarto:
            raise ValueError("Tipo do quarto inválido")

        if preco is None or preco <= 0:
            raise ValueError("Preço inválido")

        if capacidade is None or capacidade <= 0:
            raise ValueError("Capacidade inválida")

        if area_m2 is None or area_m2 <= 0:
            raise ValueError("Área inválida")

        if isinstance(tipo_quarto, str):
            try:
                tipo_quarto = TipoQuarto[tipo_quarto.upper()]
            except KeyError:
                raise ValueError("Tipo de quarto inválido. Use: STANDARD, LUXO ou SUITE")

        
        quarto = Quarto._criar(
            None,
            numero,
            tipo_quarto,
            preco,
            capacidade,
            descricao,
            andar,
            tem_varanda,
            tem_banheira,
            area_m2,
            amenidades
        )

        self._quarto_repo.salvar(quarto)

        return quarto
