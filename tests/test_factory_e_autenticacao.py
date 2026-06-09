import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import hashlib
from datetime import date
from factory.reserva_factory import ReservaFactory
from servico.servico_autenticacao import AutenticacaoServico



class HospedeMock:
    id   = 1
    nome = "Maria Souza"

class QuartoMock:
    id     = 1
    numero = 202
    preco  = 650.0

class UsuarioMock:
    def __init__(self, id, nome, email, role, senha):
        self.id    = id
        self.nome  = nome
        self.email = email
        self.role  = role
        self._senha = senha

    def verificar_senha(self, hash_recebido):
        return hash_recebido == hashlib.sha256(self._senha.encode()).hexdigest()

class UsuarioRepositorioMock:
    
    _usuarios = {
        "gerente@promissum.com":     UsuarioMock(1, "Carlos Gerente", "gerente@promissum.com",    "gerente",     "1234"),
        "funcionario@promissum.com": UsuarioMock(2, "Ana Souza",      "funcionario@promissum.com","funcionario", "1234"),
        "hospede@teste.com":         UsuarioMock(3, "Maria Hóspede",  "hospede@teste.com",        "hospede",     "4321"),
    }

    def encontrar_por_email(self, email):
        return self._usuarios.get(email, None)



def test_factory_cria_reserva_com_datas_validas():

    ci = date(2026, 10, 9)
    co = date(2026, 10, 12)
    reserva = ReservaFactory.criar_reserva(HospedeMock(), QuartoMock(), ci, co)
    assert reserva is not None
    assert reserva.total_diarias == 3


def test_factory_calcula_valor_total_corretamente():

    ci = date(2026, 10, 9)
    co = date(2026, 10, 12)
    reserva = ReservaFactory.criar_reserva(HospedeMock(), QuartoMock(), ci, co)
    assert reserva.valor_total == 1950.0


def test_factory_status_inicial_e_ativo():

    ci = date(2026, 10, 1)
    co = date(2026, 10, 5)
    reserva = ReservaFactory.criar_reserva(HospedeMock(), QuartoMock(), ci, co)
    from dominio.reserva import StatusReserva
    assert reserva.status == StatusReserva.ATIVO


#  negativos 

def test_factory_rejeita_checkout_antes_checkin():
 
    ci = date(2026, 10, 12)
    co = date(2026, 10, 9)
    with pytest.raises(ValueError, match="Check-out"):
        ReservaFactory.criar_reserva(HospedeMock(), QuartoMock(), ci, co)


def test_factory_rejeita_checkout_igual_checkin():
    ci = co = date(2026, 10, 9)
    
    with pytest.raises(ValueError, match="Check-out"):
        ReservaFactory.criar_reserva(HospedeMock(), QuartoMock(), ci, co)


def test_factory_rejeita_hospede_nulo():
    ci = date(2026, 10, 1)
    co = date(2026, 10, 5)

    with pytest.raises(ValueError, match="Hóspede"):
        ReservaFactory.criar_reserva(None, QuartoMock(), ci, co)


def test_factory_rejeita_quarto_nulo():
    ci = date(2026, 10, 1)
    co = date(2026, 10, 5)

    with pytest.raises(ValueError, match="Quarto"):
        ReservaFactory.criar_reserva(HospedeMock(), None, ci, co)


# positivos 

def test_autenticacao_aceita_gerente():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    usuario = servico.login("gerente@promissum.com", "1234")
    assert usuario.email == "gerente@promissum.com"
    assert usuario.role  == "gerente"


def test_autenticacao_aceita_funcionario():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    usuario = servico.login("funcionario@promissum.com", "1234")
    assert usuario.email == "funcionario@promissum.com"
    assert usuario.role  == "funcionario"


def test_autenticacao_aceita_hospede():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    usuario = servico.login("hospede@teste.com", "4321")
    assert usuario.email == "hospede@teste.com"
    assert usuario.role  == "hospede"


def test_autenticacao_retorna_nome_correto():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    usuario = servico.login("gerente@promissum.com", "1234")
    assert usuario.nome == "Carlos Gerente"


# negativos 

def test_autenticacao_rejeita_senha_errada():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    with pytest.raises(Exception, match="Credenciais"):
        servico.login("gerente@promissum.com", "senha_errada")


def test_autenticacao_rejeita_senha_errada_funcionario():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    with pytest.raises(Exception, match="Credenciais"):
        servico.login("funcionario@promissum.com", "errada")


def test_autenticacao_rejeita_senha_errada_hospede():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    with pytest.raises(Exception, match="Credenciais"):
        servico.login("hospede@teste.com", "1234")  


def test_autenticacao_rejeita_email_inexistente():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    with pytest.raises(Exception, match="Credenciais"):
        servico.login("naoexiste@email.com", "1234")


def test_autenticacao_rejeita_senha_vazia():

    servico = AutenticacaoServico(UsuarioRepositorioMock())
    with pytest.raises(Exception, match="Credenciais"):
        servico.login("gerente@promissum.com", "")
