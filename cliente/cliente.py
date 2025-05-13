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

def edita_produto_json(id, visivel):
    visivel = 1 if visivel else 0
    envelope = {
        "tipo_pedido" : "edita_produto",
        "id" : id,
        "visivel" : visivel,
    }
    return json.dumps(envelope).encode()

# ------------------------------------------------------------------------------

def simple_request(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f"Conectando ao servidor {HOST}:{PORT}...")
    client.connect((HOST, PORT))
    client.sendall(msg)

    resposta = client.recv(BUFSIZE).decode()
    client.close()
    return resposta

def enviar_nome(nome):
    return simple_request(nome.encode())

def login(nome, senha):
    msg = login_json(nome, senha)
    return simple_request(msg)

def edita_produto(id, visivel):
    msg = edita_produto_json(id, visivel)
    return simple_request(msg)
