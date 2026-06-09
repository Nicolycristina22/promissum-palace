import re
from dominio.hospede import Hospede


class HospedeBuilder:
    def __init__(self):
        self._nome = None
        self._documento = None
        self._email = None
        self._telefone = None
        self._endereco = None
        self._cidade = None
        self._estado = None
        self._cep = None
        self._nacionalidade = None
        self._data_nascimento = None

    def set_nome(self, nome):
        self._nome = nome
        return self

    def set_documento(self, documento):
        self._documento = documento
        return self

    def set_email(self, email):
        self._email = email
        return self

    def set_telefone(self, telefone):
        self._telefone = telefone
        return self

    def set_endereco(self, endereco):
        self._endereco = endereco
        return self

    def set_cidade(self, cidade):
        self._cidade = cidade
        return self

    def set_estado(self, estado):
        self._estado = estado
        return self

    def set_cep(self, cep):
        self._cep = cep
        return self

    def set_nacionalidade(self, nacionalidade):
        self._nacionalidade = nacionalidade
        return self

    def set_data_nascimento(self, data_nascimento):
        self._data_nascimento = data_nascimento
        return self

    def build(self):
        if not self._nome or len(self._nome.strip()) < 3:
            raise ValueError("Nome inválido (mínimo 3 caracteres)")

        
        doc_numeros = re.sub(r'[.\-/]', '', self._documento or '')
        if not doc_numeros.isdigit():
            raise ValueError("Documento deve conter apenas números (ou formatado como CPF/CNPJ)")
        if len(doc_numeros) not in [11, 14]:
            raise ValueError("Documento deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)")

        if not self._email or not self._email_valido(self._email):
            raise ValueError("Email inválido")

        if not self._telefone or len(self._telefone.strip()) < 8:
            raise ValueError("Telefone inválido (mínimo 8 caracteres)")

        if not self._endereco or len(self._endereco.strip()) < 3:
            raise ValueError("Endereço inválido")

        if not self._cidade or len(self._cidade.strip()) < 2:
            raise ValueError("Cidade inválida")

        if not self._estado or len(self._estado.strip()) < 2:
            raise ValueError("Estado inválido")

        if not self._cep or len(re.sub(r'[.\-]', '', self._cep)) < 8:
            raise ValueError("CEP inválido")

        if not self._nacionalidade or len(self._nacionalidade.strip()) < 2:
            raise ValueError("Nacionalidade inválida")

        if not self._data_nascimento:
            raise ValueError("Data de nascimento inválida")

        return Hospede._criar(
            None,
            self._nome.strip(),
            self._documento.strip(),
            self._email.strip(),
            self._telefone.strip(),
            self._endereco.strip(),
            self._cidade.strip(),
            self._estado.strip(),
            self._cep.strip(),
            self._nacionalidade.strip(),
            self._data_nascimento.strip()
        )

    def _email_valido(self, email):
        regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return isinstance(email, str) and re.match(regex, email)
