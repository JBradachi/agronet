# Adiciona diretório pai ao path do python
# Para poder acessar a biblioteca protocolo
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sqlite3
import utils as db
import logging as log
from connection import ConnectionHandler
from protocolo.protocolo import JsonTSocket

log.basicConfig(level=log.INFO)

def setup_database(conn_db):
    cur = conn_db.cursor()
    # Verifica se o banco já existe, criando-o caso não
    if not db.test_database(cur):
        db.setup_database(cur)
    cur.close()

def main():
    try:
        # Cria o banco e insere informações base
        conn_db = sqlite3.connect('./agronet.db')
        setup_database(conn_db)
        conn_db.close()
    except Exception as e:
        log.error("Erro na conexão do banco")
        log.error(e)
        exit(1)

if __name__ == "__main__":
    main()
