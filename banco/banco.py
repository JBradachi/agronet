import socket
import sqlite3
import utils as db
from connection import ConnectionHandler
import logging as log

HOST = "127.0.0.2"
PORT = 3600

log.basicConfig(level=log.INFO)

def main():
    # Associa uma porta ao socket de escuta do sistema
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    log.info(f"Servidor de dados ouvindo em {HOST}:{PORT}")

    # cria o banco e insere informações base
    try:
        conn_db = sqlite3.connect('./agronet.db')
        cursor = conn_db.cursor()
        # verifica se o banco já existe
        if not db.test_database(cursor):
            # se não existe cria um novo
            db.setup_database(cursor)
        cursor.close()
    except:
        log.error("Erro na conexão do banco")
        exit(1)

    # Servidor de dados começa a ouvir e cria uma thread a cada conexão
    while True:
        try:
            conn, addr = server.accept()
            ConnectionHandler(conn, addr)
        except:
            log.error("erro no listener")
            exit(2)

if __name__ == "__main__":
    main()
