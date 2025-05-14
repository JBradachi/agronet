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

class Cliente:
    def __init__(self):
        self.socket = None

    def setup_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log.info(f"Conectando ao servidor {HOST}:{PORT}...")
            self.socket.connect((HOST, PORT))
        except:
            log.error("Não foi possível conectar ao servidor")
            exit(64)


    def request(self, msg):
        if not self.socket:
            self.setup_socket()
        self.socket.sendall(msg)

        resposta = self.socket.recv(BUFSIZE).decode()
        if not resposta: return "nada"

        resposta = json.loads(resposta)
        return f"{resposta}"

    def enviar_nome(self, nome):
        return self.request(nome.encode())

    def login(self, nome, senha):
        msg = login_json(nome, senha)
        return self.request(msg)

    def cadastra_loja(self, nome, dia_criacao, mes_criacao, ano_criacao,
        cidade, estado, descricao):
        msg = cadastra_loja_json(nome, dia_criacao, mes_criacao, ano_criacao,
            cidade, estado, descricao)
        return self.request(msg)

    def edita_produto(self, id, visivel):
        msg = edita_produto_json(id, visivel)
        return self.request(msg)

    def insere_produto(self):
        try:
            msg = b''
            with open("gato.png", 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                msg = insere_produto_json(img_b64)
            return self.request(msg)
        except Exception as e:
            log.error(e)
            log.error("falha em insere_produto")
