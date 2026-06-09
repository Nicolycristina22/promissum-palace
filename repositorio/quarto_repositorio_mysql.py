from interfaces.quarto_repositorio_interface import QuartoRepositorioInterface
from util.conexao import Conexao
from dominio.quarto import Quarto, TipoQuarto


class QuartoRepositorioMySQL(QuartoRepositorioInterface):

    def salvar(self, quarto):
        conn   = Conexao.conectar()
        cursor = conn.cursor()

        if quarto.id is None:
            sql = """
                INSERT INTO quarto
                (numero, tipo, preco, capacidade, descricao,
                 andar, tem_varanda, tem_banheira, area_m2, amenidades)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                quarto.numero, quarto.tipo_quarto.name, quarto.preco,
                quarto.capacidade, quarto.descricao, quarto.andar,
                int(quarto.tem_varanda), int(quarto.tem_banheira),
                quarto.area_m2, quarto.amenidades
            ))
            quarto.id = cursor.lastrowid
        else:
            sql = """
                UPDATE quarto SET
                numero=%s, tipo=%s, preco=%s, capacidade=%s, descricao=%s,
                andar=%s, tem_varanda=%s, tem_banheira=%s, area_m2=%s, amenidades=%s
                WHERE id=%s
            """
            cursor.execute(sql, (
                quarto.numero, quarto.tipo_quarto.name, quarto.preco,
                quarto.capacidade, quarto.descricao, quarto.andar,
                int(quarto.tem_varanda), int(quarto.tem_banheira),
                quarto.area_m2, quarto.amenidades, quarto.id
            ))

        conn.commit()
        cursor.close()
        conn.close()

    def encontrar_por_id(self, quarto_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quarto WHERE id = %s", (quarto_id,))
        dados  = cursor.fetchone()
        cursor.close()
        conn.close()
        if not dados:
            return None
        return self._montar(dados)

    def encontrar_todos(self):
        return self.listar()

    def deletar(self, quarto_id):
        conn   = Conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM quarto WHERE id = %s", (quarto_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def listar(self):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM quarto")
        dados  = cursor.fetchall()
        cursor.close()
        conn.close()
        return [self._montar(d) for d in dados]


    def _montar(self, d):
        tipo = TipoQuarto[d["tipo"].upper()] if d["tipo"] else TipoQuarto.STANDARD
        return Quarto._criar(
            d["id"], d["numero"], tipo,
            float(d["preco"]      or 0),
            int(d["capacidade"]   or 1),
            d["descricao"]        or "",
            int(d["andar"]        or 1),
            bool(d["tem_varanda"]),
            bool(d["tem_banheira"]),
            float(d["area_m2"]    or 0),
            d["amenidades"]       or ""
        )
