import socket
import logging

HOST = "127.0.0.1"
PORT = 6000

logging.basicConfig(level=logging.INFO)

def enviar_nome(nome):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Conectando ao servidor {HOST}:{PORT}...")

    client.connect((HOST, PORT))

    client.sendall(nome.encode())
    resposta = client.recv(1024).decode()

    client.close()
    return resposta
