from interfaces.usuario_repositorio_interface import UsuarioRepositorioInterface
from util.conexao import Conexao
from dominio.usuario import Usuario


class UsuarioRepositorioMySQL(UsuarioRepositorioInterface):

    def encontrar_por_email(self, email: str):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE email = %s", (email,))
        dados  = cursor.fetchone()
        cursor.close()
        conn.close()
        if not dados:
            return None
        return self._montar(dados)

    def encontrar_por_id(self, usuario_id: int):
        conn   = Conexao.conectar()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE id = %s", (usuario_id,))
        dados  = cursor.fetchone()
        cursor.close()
        conn.close()
        if not dados:
            return None
        return self._montar(dados)

    def salvar(self, usuario):
        conn   = Conexao.conectar()
        cursor = conn.cursor()
        if usuario.id is None:
            sql = """
                INSERT INTO usuario
                (nome, documento, email, senha, role, telefone, endereco,
                 cidade, estado, cep, nacionalidade, data_nascimento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                usuario.nome, usuario.documento, usuario.email,
                usuario.senha_hash, usuario.role, usuario.telefone,
                usuario.endereco, usuario.cidade, usuario.estado,
                usuario.cep, usuario.nacionalidade, usuario.data_nascimento
            ))
            usuario.id = cursor.lastrowid
        else:
            sql = """
                UPDATE usuario SET
                nome=%s, documento=%s, email=%s, telefone=%s,
                endereco=%s, cidade=%s, estado=%s, cep=%s, nacionalidade=%s
                WHERE id=%s
            """
            cursor.execute(sql, (
                usuario.nome, usuario.documento, usuario.email,
                usuario.telefone, usuario.endereco, usuario.cidade,
                usuario.estado, usuario.cep, usuario.nacionalidade,
                usuario.id
            ))
        conn.commit()
        cursor.close()
        conn.close()

    def _montar(self, d):
        return Usuario._criar(
            d["id"],
            d["nome"]            or "",
            d["documento"]       or "",
            d["email"]           or "",
            d["senha"]           or "",
            d["role"]            or "hospede",
            d["telefone"]        or "",
            d["endereco"]        or "",
            d["cidade"]          or "",
            d["estado"]          or "",
            d["cep"]             or "",
            d["nacionalidade"]   or "",
            str(d["data_nascimento"]) if d.get("data_nascimento") else ""
        )
