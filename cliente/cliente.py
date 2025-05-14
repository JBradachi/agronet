import base64
import socket
import logging as log
import json

HOST = "127.0.0.1"
PORT = 6000
BUFSIZE = 4096

log.basicConfig(level=log.INFO)

def login_json(nome, senha):
    envelope = { 
        "tipo_pedido" : "login", 
        "nome" : nome, 
        "senha" : senha 
    }
    return json.dumps(envelope).encode()

def edita_produto_json(id, visivel):
    visivel = 1 if visivel else 0
    envelope = {
        "tipo_pedido" : "edita_produto",
        "id" : id,
        "visivel" : visivel,
    }
    return json.dumps(envelope).encode()

def insere_produto_json(imagem):
    envelope = { 
        "tipo_pedido" : "cadastro_produto", 
        "modelo" : "Challenger MT525D 4WD", 
        "preco" : 77.8, 
        "mes_fabricacao" : 2,
        "ano_fabricacao" : 2004, 
        "nome_imagem" : "gato.png",
        "imagem" : imagem 
    }
    return json.dumps(envelope).encode()

# ------------------------------------------------------------------------------

def simple_request(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info(f"Conectando ao servidor {HOST}:{PORT}...")
    client.connect((HOST, PORT))
    client.sendall(msg)

    resposta = client.recv(BUFSIZE).decode()
    resposta = json.loads(resposta)
    
    client.close()
    return f"{resposta}"

def insert_product_request(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info(f"Conectando ao servidor {HOST}:{PORT}...")
    client.connect((HOST, PORT))
    client.sendall(msg)
    
    resposta = client.recv(BUFSIZE).decode()
    resposta = json.loads(resposta)
    client.close()
    return f"{resposta}"

def enviar_nome(nome):
    return simple_request(nome.encode())

def login(nome, senha):
    msg = login_json(nome, senha)
    return simple_request(msg)

def edita_produto(id, visivel):
    msg = edita_produto_json(id, visivel)
    return simple_request(msg)

def insere_produto():
    try:
        msg = b''
        with open("gato.png", 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
            msg = insere_produto_json(img_b64)
        return insert_product_request(msg)
    except Exception as e:
        log.error(e)
        log.error("falha em insere_produto")
