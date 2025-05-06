import socket
from connection import Connection

HOST = "0.0.0.0"  
PORT = 6000

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor ouvindo em {HOST}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            connection = Connection(conn, addr)
        except:
            print("erro no listener")

if __name__ == "__main__":
    main()