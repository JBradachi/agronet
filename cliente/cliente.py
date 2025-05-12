import socket
import logging
import json

HOST = "127.0.0.1"
PORT = 6000
BUFSIZE = 4096

logging.basicConfig(level=logging.INFO)

def login_json(nome, senha):
    envelope = { "tipo_pedido" : "login", "nome" : nome, "senha" : senha }
    return json.dumps(envelope).encode()

def enviar_nome(nome):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Conectando ao servidor {HOST}:{PORT}...")

    client.connect((HOST, PORT))

    client.sendall(nome.encode())
    resposta = client.recv(BUFSIZE).decode()

    client.close()
    return resposta

def login(nome, senha):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Conectando ao servidor {HOST}:{PORT}...")

    client.connect((HOST, PORT))

    validacao = login_json(nome, senha)

    client.sendall(validacao)
    resposta = client.recv(BUFSIZE).decode()

    client.close()
    return resposta



