import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from decorator.reserva_basica import ReservaBasica
from decorator.servicos_extras import CafeDaManha, Estacionamento, LateCheckout, TransferAeroporto


class ReservaMock:
    def __init__(self, valor=350.0, diarias=2):
        self.valor_total  = valor
        self.total_diarias = diarias
        class QuartoMock:
            numero = 101
        self.quarto = QuartoMock()

def test_reserva_basica_retorna_valor_original():
    mock = ReservaMock(valor=350.0)
    base = ReservaBasica(mock)
    assert base.custo() == 350.0


def test_reserva_basica_descricao_contem_numero_quarto():
    mock = ReservaMock()
    base = ReservaBasica(mock)
    assert "101" in base.get_descricao()


def test_cafe_da_manha_soma_50():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = CafeDaManha(base)
    assert decorado.custo() == 400.0


def test_estacionamento_soma_30():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = Estacionamento(base)
    assert decorado.custo() == 380.0


def test_late_checkout_soma_80():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = LateCheckout(base)
    assert decorado.custo() == 430.0


def test_transfer_aeroporto_soma_120():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = TransferAeroporto(base)
    assert decorado.custo() == 470.0


def test_empilhar_cafe_e_estacionamento():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = Estacionamento(CafeDaManha(base))
    assert decorado.custo() == 430.0


def test_empilhar_todos_os_servicos():
    base = ReservaBasica(ReservaMock(valor=350.0))
    decorado = TransferAeroporto(LateCheckout(Estacionamento(CafeDaManha(base))))
    assert decorado.custo() == 630.0  # 350 + 50 + 30 + 80 + 120


def test_descricao_acumula_servicos():
    base = ReservaBasica(ReservaMock())
    decorado = Estacionamento(CafeDaManha(base))
    assert "Café da manhã" in decorado.get_descricao()
    assert "Estacionamento" in decorado.get_descricao()

def test_sem_servicos_nao_soma_nada():
    base = ReservaBasica(ReservaMock(valor=500.0))
    assert base.custo() == 500.0  # valor não deve mudar


def test_descricao_sem_servicos_nao_contem_extras():
    base = ReservaBasica(ReservaMock())
    assert "Café" not in base.get_descricao()
    assert "Estacionamento" not in base.get_descricao()
