import base64
import socket
import logging as log
import json
import struct

HOST = "127.0.0.1"
PORT = 6000
PAYLOAD_SIZE = struct.calcsize("Q")

log.basicConfig(level=log.INFO)

def monta_frame(dados):
    dados_bin = json.dumps(dados).encode()
    tamanho_msg = struct.pack("Q", len(dados_bin))
    
    return tamanho_msg+dados_bin

def receba(socket):
    msg_size = socket.recv(PAYLOAD_SIZE)
    if not msg_size:
        return msg_size
    msg_size = struct.unpack("Q", msg_size)[0]

    resposta = socket.recv(msg_size).decode()
    return resposta


def login_json(nome, senha):
    envelope = { 
        "tipo_pedido" : "login", 
        "nome" : nome, 
        "senha" : senha 
    }
    return monta_frame(envelope)

def cadastra_loja_json(nome, dia_criacao, mes_criacao, ano_criacao,
   cidade, estado, descricao):
    envelope = {
        "tipo_pedido" : "cadastra_loja",
        "nome" : nome,
        "dia_criacao" : dia_criacao,
        "mes_criacao" : mes_criacao,
        "ano_criacao" : ano_criacao,
        "cidade" : cidade,
        "estado" : estado,
        "descricao" : descricao,
    }
    return monta_frame(envelope)

def edita_produto_json(id, visivel):
    visivel = 1 if visivel else 0
    envelope = {
        "tipo_pedido" : "edita_produto",
        "id" : id,
        "visivel" : visivel,
    }
    return monta_frame(envelope)

def insere_produto_json(imagem, modelo, preco, mes_fabricacao, ano_fabricacao, 
                        nome_imagem):
    envelope = { 
        "tipo_pedido" : "cadastro_produto", 
        "modelo" : modelo,
        "preco" : preco,
        "mes_fabricacao" : mes_fabricacao,
        "ano_fabricacao" : ano_fabricacao,
        "nome_imagem" : nome_imagem,
        "imagem" : imagem 
    }
    return monta_frame(envelope)

# ------------------------------------------------------------------------------

def simple_request(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info(f"Conectando ao servidor {HOST}:{PORT}...")
    client.connect((HOST, PORT))

    client.sendall(msg)

    resposta = receba(client)
    if not resposta:
        resposta = { "status" : "resposta vazia" }
    else: resposta = json.loads(resposta)
    
    client.close()
    return f"{resposta}"

def insert_product_request(msg):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info(f"Conectando ao servidor {HOST}:{PORT}...")
    client.connect((HOST, PORT))

    client.sendall(msg) 
    
    resposta = receba(client)
    if not resposta:
        resposta = { "status" : "resposta vazia" }
        log.info(f"resposta vazia {resposta}")
    else: 
        resposta = json.loads(resposta)
        log.info(f"resposta certa {resposta}")

    client.close()
    return f"{resposta}"

def enviar_nome(nome):
    return simple_request(nome.encode())

def login(nome, senha):
    msg = login_json(nome, senha)
    return simple_request(msg)

def cadastra_loja(nome, dia_criacao, mes_criacao, ano_criacao,
    cidade, estado, descricao):

    msg = cadastra_loja_json(nome, dia_criacao, mes_criacao, ano_criacao,
        cidade, estado, descricao)
    return simple_request(msg)

def edita_produto(id, visivel):
    msg = edita_produto_json(id, visivel)
    return simple_request(msg)

def insere_produto():
    try:

        modelo = "Challenger MT525D 4WD"
        preco = 77.8
        mes_fabricacao = 2
        ano_fabricacao = 2004 
        nome_imagem = "gato.png"

        msg = b''
        with open("gato.png", 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode('utf-8')
            msg = insere_produto_json(img_b64, modelo, preco, mes_fabricacao, ano_fabricacao, nome_imagem)
        return insert_product_request(msg)
    
    except Exception as e:
        log.error(e)
        log.error("falha em insere_produto")
