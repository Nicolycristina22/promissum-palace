class Usuario:

    def __init__(self, *args, **kwargs):
        raise Exception("Use UsuarioBuilder para criar o usuário")

    @classmethod
    def _criar(cls, usuario_id, nome, documento, email, senha_hash, role,
               telefone, endereco, cidade, estado, cep, nacionalidade, data_nascimento):
        obj = cls.__new__(cls)
        obj._id              = usuario_id
        obj._nome            = nome
        obj._documento       = documento
        obj._email           = email
        obj._senha_hash      = senha_hash
        obj._role            = role
        obj._telefone        = telefone
        obj._endereco        = endereco
        obj._cidade          = cidade
        obj._estado          = estado
        obj._cep             = cep
        obj._nacionalidade   = nacionalidade
        obj._data_nascimento = data_nascimento
        return obj

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if self._id is not None:
            raise ValueError("ID já definido, não pode ser alterado")
        self._id = value

    @property
    def nome(self):
        return self._nome

    @property
    def documento(self):
        return self._documento

    @property
    def email(self):
        return self._email

    @property
    def senha_hash(self):
        return self._senha_hash

    @property
    def role(self):
        return self._role

    @property
    def telefone(self):
        return self._telefone

    @property
    def endereco(self):
        return self._endereco

    @property
    def cidade(self):
        return self._cidade

    @property
    def estado(self):
        return self._estado

    @property
    def cep(self):
        return self._cep

    @property
    def nacionalidade(self):
        return self._nacionalidade

    @property
    def data_nascimento(self):
        return self._data_nascimento

    def verificar_senha(self, senha_hash: str) -> bool:
        return self._senha_hash == senha_hash
