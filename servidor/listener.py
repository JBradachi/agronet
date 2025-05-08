import socket
from connection import Connection
import logging as log

HOST = "127.0.0.1" 
PORT = 6000
log.basicConfig(level=log.INFO)

def main():
    
    # Associa uma porta ao socket de escuta do sistema 
    # (TCP == socket.SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    log.info(f"Servidor de aplicação ouvindo em {HOST}:{PORT}")
    
    # Servidor começa a ouvir e cria uma thread a cada conexão
    while True:
        try:
            conn, addr = server.accept()
            connection = Connection(conn, addr)
            
        except:
            log.error("erro no listener")
            exit(2)

if __name__ == "__main__":
    main()