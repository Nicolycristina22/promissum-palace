import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from builder.hospede_builder import HospedeBuilder
DADOS_VALIDOS = dict(
    nome="João Silva",
    documento="123.456.789-09",
    email="joao@email.com",
    telefone="11912345678",
    endereco="Rua das Flores, 100",
    cidade="São Paulo",
    estado="SP",
    cep="01310-100",
    nacionalidade="Brasileiro",
    data_nascimento="2000-01-01"
)

def builder_valido():
    b = HospedeBuilder()
    for k, v in DADOS_VALIDOS.items():
        getattr(b, f"set_{k}")(v)
    return b

def test_builder_cria_hospede_com_dados_validos():
    b = builder_valido()
    hospede = b.build()
    assert hospede.nome == "João Silva"
    assert hospede.email == "joao@email.com"


def test_builder_aceita_cpf_formatado():
    b = builder_valido().set_documento("111.111.111-11")
    hospede = b.build()
    assert hospede is not None


def test_builder_retorna_objeto_hospede():
    b = builder_valido()
    hospede = b.build()
    from dominio.hospede import Hospede
    assert isinstance(hospede, Hospede)

def test_builder_rejeita_nome_curto():
    b = builder_valido().set_nome("Jo")
    with pytest.raises(ValueError, match="Nome"):
        b.build()


def test_builder_rejeita_email_sem_arroba():
    b = builder_valido().set_email("emailsemarroba.com")
    with pytest.raises(ValueError, match="Email"):
        b.build()


def test_builder_rejeita_cpf_com_letras():
    b = builder_valido().set_documento("abc.def.ghi-jk")
    with pytest.raises(ValueError, match="Documento"):
        b.build()


def test_builder_rejeita_cpf_com_digitos_insuficientes():
    b = builder_valido().set_documento("12345")
    with pytest.raises(ValueError, match="Documento"):
        b.build()


def test_builder_rejeita_telefone_curto():
    b = builder_valido().set_telefone("123")
    with pytest.raises(ValueError, match="Telefone"):
        b.build()


def test_builder_rejeita_cep_invalido():
    b = builder_valido().set_cep("123")
    with pytest.raises(ValueError, match="CEP"):
        b.build()


def test_builder_rejeita_sem_data_nascimento():
    b = builder_valido().set_data_nascimento(None)
    with pytest.raises(ValueError, match="nascimento"):
        b.build()
