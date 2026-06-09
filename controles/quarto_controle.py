class QuartoControle:
    def __init__(self, criar_command, repositorio):
        self._criar_command = criar_command
        self._repositorio = repositorio

    def criar_quarto(self, numero, tipo, preco, capacidade, descricao, andar, tem_varanda, tem_banheira, area_m2, amenidades):
        return self._criar_command.executar(numero, tipo, preco, capacidade, descricao, andar, tem_varanda, tem_banheira, area_m2, amenidades)

    def buscar_por_id(self, quarto_id):
        quarto = self._repositorio.encontrar_por_id(quarto_id)
        if not quarto:
            raise Exception("Quarto não encontrado")
        return quarto

    def atualizar_quarto(self, quarto_id, novo_preco=None, nova_descricao=None):
        quarto = self._repositorio.encontrar_por_id(quarto_id)
        if not quarto:
            raise Exception("Quarto não encontrado")
        if novo_preco is not None:
            quarto.atualizar_preco(novo_preco)
        if nova_descricao:
            quarto.atualizar_descricao(nova_descricao)
        self._repositorio.salvar(quarto)
        return quarto

    def deletar_quarto(self, quarto_id):
        quarto = self._repositorio.encontrar_por_id(quarto_id)
        if not quarto:
            raise Exception("Quarto não encontrado")
        self._repositorio.deletar(quarto_id)

    def listar_quartos(self):
        return self._repositorio.listar()
