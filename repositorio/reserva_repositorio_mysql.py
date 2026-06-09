from datetime import datetime, date
from interfaces.reserva_repositorio_interface import ReservaRepositorioInterface
from util.conexao import Conexao
from dominio.reserva import Reserva, StatusReserva
from repositorio.hospede_repositorio_mysql import HospedeRepositorioMySQL
from repositorio.quarto_repositorio_mysql  import QuartoRepositorioMySQL


class ReservaRepositorioMySQL(ReservaRepositorioInterface):


    def __init__(self):
        self.hospede_repo = HospedeRepositorioMySQL()
        self.quarto_repo  = QuartoRepositorioMySQL()
    def _salvar_servicos(self, cursor, reserva_id, servicos: list):
        cursor.execute("DELETE FROM reserva_servico WHERE reserva_id = %s", (reserva_id,))
        for s in servicos:
            cursor.execute(
                "INSERT INTO reserva_servico (reserva_id, servico_key) VALUES (%s, %s)",
                (reserva_id, s)
            )

    def _carregar_servicos(self, cursor, reserva_id) -> list:
        cursor.execute(
            "SELECT servico_key FROM reserva_servico WHERE reserva_id = %s",
            (reserva_id,)
        )
        return [row["servico_key"] for row in cursor.fetchall()]
    def salvar(self, reserva, servicos_extras=None):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)

        if reserva.id is None:
            sql = """
                INSERT INTO reserva
                (hospede_id, quarto_id, check_in, check_out, status,
                 total_diarias, valor_total, observacao, forma_pagamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                reserva.hospede.id, reserva.quarto.id,
                reserva.check_in, reserva.check_out,
                reserva.status.value,
                reserva.total_diarias,
                float(reserva.valor_total),
                reserva.observacao      or "",
                reserva.forma_pagamento or "PIX"
            ))
            reserva.id = cursor.lastrowid
        else:
            sql = """
                UPDATE reserva SET
                check_in=%s, check_out=%s, status=%s,
                total_diarias=%s, valor_total=%s,
                observacao=%s, forma_pagamento=%s
                WHERE id=%s
            """
            cursor.execute(sql, (
                reserva.check_in, reserva.check_out,
                reserva.status.value,
                reserva.total_diarias,
                float(reserva.valor_total),
                reserva.observacao      or "",
                reserva.forma_pagamento or "PIX",
                reserva.id
            ))

        if servicos_extras is not None:
            self._salvar_servicos(cursor, reserva.id, servicos_extras)

        conn.commit()
        cursor.close()
        conn.close()
    def encontrar_por_id(self, reserva_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reserva WHERE id = %s", (int(reserva_id),))
        dados  = cursor.fetchone()
        if not dados:
            cursor.close(); conn.close(); return None
        servicos = self._carregar_servicos(cursor, dados["id"])
        cursor.close(); conn.close()
        return self._montar(dados, servicos)

    def encontrar_todos(self):
        return self.listar()

    def encontrar_por_quarto(self, quarto_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reserva WHERE quarto_id = %s", (int(quarto_id),))
        dados  = cursor.fetchall()
        result = [self._montar(d, self._carregar_servicos(cursor, d["id"])) for d in dados]
        cursor.close(); conn.close()
        return result

    def encontrar_por_hospede(self, hospede_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reserva WHERE hospede_id = %s", (int(hospede_id),))
        dados  = cursor.fetchall()
        result = [self._montar(d, self._carregar_servicos(cursor, d["id"])) for d in dados]
        cursor.close(); conn.close()
        return result

    def deletar(self, reserva_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reserva WHERE id = %s", (int(reserva_id),))
        conn.commit()
        cursor.close(); conn.close()

    def listar(self):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM reserva")
        dados  = cursor.fetchall()
        result = [self._montar(d, self._carregar_servicos(cursor, d["id"])) for d in dados]
        cursor.close(); conn.close()
        return result

    def atualizar_servicos(self, reserva_id, servicos: list, novo_valor_total: float = None):
        conn   = Conexao.conectar()
        cursor = conn.cursor()
        self._salvar_servicos(cursor, reserva_id, servicos)
        if novo_valor_total is not None:
            cursor.execute(
                "UPDATE reserva SET valor_total = %s WHERE id = %s",
                (float(novo_valor_total), int(reserva_id))
            )
        conn.commit()
        cursor.close(); conn.close()

    def _montar(self, d, servicos=None):
        hospede = self.hospede_repo.encontrar_por_id(d["hospede_id"])
        quarto  = self.quarto_repo.encontrar_por_id(d["quarto_id"])
        status  = StatusReserva(d["status"])
        reserva = Reserva._criar(
            d["id"], hospede, quarto,
            self._to_date(d["check_in"]),
            self._to_date(d["check_out"]),
            status,
            int(d["total_diarias"]   or 0),
            float(d["valor_total"]   or 0),
            d["observacao"]          or "",
            d["forma_pagamento"]     or "PIX"
        )
        reserva.set_servicos_extras(servicos or [])
        return reserva

    @staticmethod
    def _to_date(valor):
        if valor is None:
            return None
        if isinstance(valor, date):
            return valor
        return datetime.strptime(str(valor), "%Y-%m-%d").date()
