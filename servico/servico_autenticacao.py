import hashlib


class AutenticacaoServico:

    def __init__(self, usuario_repositorio):
        self._usuario_repositorio = usuario_repositorio

    def login(self, email: str, senha: str):
        usuario = self._usuario_repositorio.encontrar_por_email(email)
        if not usuario:
            raise Exception("Credenciais inválidas")
        senha_hash = self._hash(senha)
        if not usuario.verificar_senha(senha_hash):
            raise Exception("Credenciais inválidas")
        return usuario

    @staticmethod
    def _hash(senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()
