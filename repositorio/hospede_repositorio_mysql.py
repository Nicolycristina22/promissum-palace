from datetime import datetime
from interfaces.hospede_repositorio_interface import HospedeRepositorioInterface
from util.conexao import Conexao
from dominio.hospede import Hospede


class HospedeRepositorioMySQL(HospedeRepositorioInterface):

    def salvar(self, hospede):
        conn   = Conexao.conectar()
        cursor = conn.cursor()

        data_nasc = self._converter_data(hospede.data_nascimento)

        if hospede.id is None:
            sql = """
                INSERT INTO hospede
                (nome, documento, email, telefone, endereco,
                 cidade, estado, cep, nacionalidade, data_nascimento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                hospede.nome, hospede.documento, hospede.email,
                hospede.telefone, hospede.endereco, hospede.cidade,
                hospede.estado, hospede.cep, hospede.nacionalidade, data_nasc
            ))
            hospede.id = cursor.lastrowid

        else:
            sql = """
                UPDATE hospede SET
                nome=%s, documento=%s, email=%s, telefone=%s, endereco=%s,
                cidade=%s, estado=%s, cep=%s, nacionalidade=%s, data_nascimento=%s
                WHERE id=%s
            """
            cursor.execute(sql, (
                hospede.nome, hospede.documento, hospede.email,
                hospede.telefone, hospede.endereco, hospede.cidade,
                hospede.estado, hospede.cep, hospede.nacionalidade,
                data_nasc, hospede.id
            ))

        conn.commit()
        cursor.close()
        conn.close()

    def encontrar_por_id(self, hospede_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hospede WHERE id = %s", (hospede_id,))
        dados  = cursor.fetchone()
        cursor.close()
        conn.close()
        if not dados:
            return None
        return self._montar(dados)

    def deletar(self, hospede_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hospede WHERE id = %s", (hospede_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def encontrar_por_email(self, email: str):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hospede WHERE email = %s", (email,))
        dados  = cursor.fetchone()
        cursor.close(); conn.close()
        return self._montar(dados) if dados else None

    def listar(self):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM hospede")
        dados = cursor.fetchall()
        cursor.close()
        conn.close()
        return [self._montar(d) for d in dados]

    

    def _montar(self, d):
        return Hospede._criar(
            d["id"],
            d["nome"]           or "",
            d["documento"]      or "",
            d["email"]          or "",
            d["telefone"]       or "",
            d["endereco"]       or "",
            d["cidade"]         or "",
            d["estado"]         or "",
            d["cep"]            or "",
            d["nacionalidade"]  or "",
            str(d["data_nascimento"]) if d["data_nascimento"] else ""
        )

    @staticmethod
    def _converter_data(valor):
        if valor is None or valor == "":
            return None
        if hasattr(valor, "year"):
            return valor
        valor = str(valor).strip()
        if "/" in valor:
            return datetime.strptime(valor, "%d/%m/%Y").date()
        if "-" in valor:
            return datetime.strptime(valor, "%Y-%m-%d").date()
        return None
