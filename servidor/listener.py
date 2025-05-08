import socket
import sqlite3
from connection import Connection
import db.db

HOST = "0.0.0.0"  
PORT = 6000

def main():
    
    # Associa uma porta ao socket de escuta do sistema 
    # (TCP == socket.SOCK_STREAM)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    # cria o banco e insere informações base
    try:
        conn_db = sqlite3.connect('./db/agronet.db')
        cursor = conn_db.cursor()
        db.db.setup_database(cursor)    
        cursor.close()

    except:
        print("Erro na conexão do banco")
        print("Certifique que o banco não será duplicado")
        exit(1)
    
    # Servidor começa a ouvir e cria uma thread a cada conexão
    while True:
        try:
            conn, addr = server.accept()
            connection = Connection(conn, addr)
            
        except:
            print("erro no listener")
            exit(2)

if __name__ == "__main__":
    main()