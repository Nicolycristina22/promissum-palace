class Hospede:

    def __init__(self, *args, **kwargs):
        raise Exception("Use HospedeBuilder para criar o hóspede")

    @classmethod
    def _criar(cls, hospede_id, nome, documento, email, telefone, endereco, cidade, estado, cep, nacionalidade, data_nascimento):
        obj = cls.__new__(cls)
        obj._id             = hospede_id
        obj._nome           = nome
        obj._documento      = documento
        obj._email          = email
        obj._telefone       = telefone
        obj._endereco       = endereco
        obj._cidade         = cidade
        obj._estado         = estado
        obj._cep            = cep
        obj._nacionalidade  = nacionalidade
        obj._data_nascimento = data_nascimento
        return obj

    def __str__(self):
        return f"Nome: {self._nome}, Documento: {self._documento}, Email: {self._email}, Telefone: {self._telefone}"


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


    def atualizar_email(self, novo_email: str):
        if not self._email_valido(novo_email):
            raise ValueError("Email inválido")
        self._email = novo_email

    def atualizar_telefone(self, novo_telefone: str):
        if not novo_telefone or len(novo_telefone.strip()) < 8:
            raise ValueError("Telefone inválido")
        self._telefone = novo_telefone.strip()

    def atualizar_endereco(self, novo_endereco: str):
        if not novo_endereco or len(novo_endereco.strip()) < 3:
            raise ValueError("Endereço inválido")
        self._endereco = novo_endereco.strip()

    @staticmethod
    def _email_valido(email: str):
        return isinstance(email, str) and "@" in email and "." in email

    @staticmethod
    def _telefone_valido(telefone: str):
        return isinstance(telefone, str) and len(telefone.strip()) >= 8

    @staticmethod
    def _endereco_valido(endereco: str):
        return isinstance(endereco, str) and len(endereco.strip()) >= 3
