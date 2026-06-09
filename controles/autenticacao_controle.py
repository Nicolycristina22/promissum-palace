from servico.servico_autenticacao import AutenticacaoServico


class AutenticacaoControle:

    def __init__(self, usuario_repositorio):
        self._servico = AutenticacaoServico(usuario_repositorio)

    def login(self, email: str, senha: str):
        return self._servico.login(email, senha)
