import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
from connection import ConnectionHandler
import logging as log
from protocolo.protocolo import JsonTSocket

HOST = "127.0.0.1"
PORT = 6000
log.basicConfig(level=log.INFO)

def main():
    # Associa uma porta ao socket de escuta do sistema
    # (TCP == socket.SOCK_STREAM)
    # (IPv4 == socket.AF_INET)
    server = JsonTSocket()
    server.bind(HOST, PORT)
    server.listen()

    log.info(f"Servidor de aplicação ouvindo em {HOST}:{PORT}")
    while True:
        try:
            conn, addr = server.accept()
            # A criação do objeto ConnectionHandler cria uma thread dedicada
            # para lidar com a conexão
            ConnectionHandler(conn, addr)
        except:
            log.error("erro no listener")
            exit(2)

if __name__ == "__main__":
    main()
