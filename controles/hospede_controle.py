from builder.hospede_builder import HospedeBuilder


class HospedeControle:
    def __init__(self, repositorio):
        self._repositorio = repositorio

   

    def criar_hospede(
        self, nome, documento, email, telefone, endereco,
        cidade, estado, cep, nacionalidade, data_nascimento
    ):
        hospede = (
            HospedeBuilder()
            .set_nome(nome)
            .set_documento(documento)
            .set_email(email)
            .set_telefone(telefone)
            .set_endereco(endereco)
            .set_cidade(cidade)
            .set_estado(estado)
            .set_cep(cep)
            .set_nacionalidade(nacionalidade)
            .set_data_nascimento(data_nascimento)
            .build()
        )

        self._repositorio.salvar(hospede)  
        return hospede

   

    def buscar_por_id(self, hospede_id):
        hospede = self._repositorio.encontrar_por_id(hospede_id)

        if not hospede:
            raise Exception("Hóspede não encontrado")

        return hospede

    

    def atualizar_hospede(
        self,
        hospede_id,
        novo_email=None,
        novo_telefone=None,
        novo_endereco=None,
        novo_nome=None,
        nova_cidade=None,
        novo_estado=None,
        novo_cep=None,
        nova_nacionalidade=None
    ):
        hospede = self._repositorio.encontrar_por_id(hospede_id)

        if not hospede:
            raise Exception("Hóspede não encontrado")

        if novo_email:
            hospede.atualizar_email(novo_email)
        if novo_telefone:
            hospede.atualizar_telefone(novo_telefone)
        if novo_endereco:
            hospede.atualizar_endereco(novo_endereco)
        if novo_nome:
            hospede._nome = novo_nome.strip()
        if nova_cidade:
            hospede._cidade = nova_cidade.strip()
        if novo_estado:
            hospede._estado = novo_estado.strip()
        if novo_cep:
            hospede._cep = novo_cep.strip()
        if nova_nacionalidade:
            hospede._nacionalidade = nova_nacionalidade.strip()

        self._repositorio.salvar(hospede)

        return hospede


    def deletar_hospede(self, hospede_id):
        hospede = self._repositorio.encontrar_por_id(hospede_id)

        if not hospede:
            raise Exception("Hóspede não encontrado")

        self._repositorio.deletar(hospede_id)


    def listar_hospedes(self):
        return self._repositorio.listar()
