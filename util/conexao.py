import mysql.connector

class Conexao:
    _config = {
        "host": "localhost",
        "user": "root",
        "password": "",
        "database": "promissum_palace",
        "port": 3309
    }

    @staticmethod
    def conectar():
        return mysql.connector.connect(**Conexao._config)
