# Adiciona diretório pai ao path do python
# Para poder acessar a biblioteca protocolo
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import logging as log
from protocolo.protocolo import JsonTSocket

from protocolo.loja import Loja
from protocolo.usuario import Usuario
from protocolo.maquina import Maquina

HOST = "127.0.0.1"
PORT = 6000

log.basicConfig(level=log.INFO)

class Cliente:
    def __init__(self):
        self.socket = None

    def setup_socket(self):
        try:
            self.socket = JsonTSocket()
            log.info(f"Conectando ao servidor {HOST}:{PORT}...")
            self.socket.connect(HOST, PORT)
        except:
            log.error("Não foi possível conectar ao servidor")
            exit(64)

    def request(self, data):
        if not self.socket:
            self.setup_socket()
        self.socket.send_dict(data)
        resposta = self.socket.recv_dict()
        return resposta

    def login(self, nome, senha):
        usuario = Usuario(nome, senha)
        data = usuario.dict()
        data["tipo_pedido"] = "login"
        return self.request(data)

    def cadastra_loja(self, nome, dia_criacao, mes_criacao, ano_criacao,
        cidade, estado, descricao):
        loja = Loja(nome, dia_criacao, mes_criacao, ano_criacao,
            cidade, estado, descricao)
        req = loja.dict()
        req["tipo_pedido"] = "cadastra_loja"
        return self.request(req)

    def edita_produto(self, id, visivel):
        return self.request({
            "tipo_pedido" : "edita_produto",
            "id" : id,
            "visivel" : bool(visivel),
        })

    def insere_produto(self):
        loja = "adminStore"
        modelo = "Challenger MT525D 4WD"
        preco = 77.8
        mes_fabricacao = 2
        ano_fabricacao = 2004
        nome_imagem = "gato.png"
        produto = Maquina(loja, modelo, nome_imagem, preco,
            mes_fabricacao, ano_fabricacao, True)

        # Convertendo para o dicionário adequado
        data = produto.dict()
        data["tipo_pedido"] = "cadastro_produto"
        try:
            with open("gato.png", 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                data["imagem_conteudo"] = img_b64
            return self.request(data)
        except Exception as e:
            log.error(e)
            log.error("falha em insere_produto")
