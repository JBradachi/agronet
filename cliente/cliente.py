# Adiciona diretório pai ao path do python
# Para poder acessar a biblioteca protocolo
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import logging as log

from protocolo.protocolo import JsonTSocket
from protocolo.entidades import Loja, Usuario, Maquina
from threading import Thread

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
        resposta = self.request(data)

        if resposta.get("status") == 0:
            self.usuario_logado = {
                "nome": nome,
                "loja": resposta.get("loja"),
                "token": resposta.get("token")
            }
        else:
            self.usuario_logado = None

        return resposta

    def cadastra_usuario(self, nome, senha):
        usuario = Usuario(nome, senha)
        data = usuario.dict()
        data["tipo_pedido"] = "cadastra_usuario"
        return self.request(data)

    def cadastra_loja(self, nome, dia_criacao, mes_criacao, ano_criacao,
        cidade, estado, descricao):
        loja = Loja(nome, dia_criacao, mes_criacao, ano_criacao,
            cidade, estado, descricao)
        req = loja.dict()
        req["tipo_pedido"] = "cadastra_loja"
        return self.request(req)

    def edita_produto(self, id, visivel):
        log.info(f"MUDANÇA DE VISIBILIDADE ID: {id} VISIB: {visivel}")
        return self.request({
            "tipo_pedido" : "edita_produto",
            "id" : id,
            "visivel" : bool(visivel),
        })

    # TODO: na integração add os parametros
    # loja, modelo, preco, mes_fabricacao, ano_fabricacao, nome_imagem
    def insere_produto(self, loja, modelo, preco, mes_fabricacao, ano_fabricacao, nome_imagem, quantidade):
        produto = Maquina(loja, modelo, nome_imagem, preco, mes_fabricacao, ano_fabricacao, True, quantidade)
        data = produto.dict()
        data["tipo_pedido"] = "cadastra_produto"

        try:
            with open(f"static/{produto.imagem}", 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                data["imagem_conteudo"] = img_b64
            return self.request(data)
        except Exception as e:
            log.error(e)
            log.error("falha em insere_produto")


    # a partir de um id de máquina, retorna todas as info delas
    # em um dicionário
    # TODO: na integração adicionar id como parametro
    def requisita_produto_completo(self, id):
        data = { "tipo_pedido" : "requisita_produto", "id" : id }
        data = self.request(data)

        nome_imagem = busca_nome_imagem(data)
        if nome_imagem not in os.listdir("static"):
            self.baixa_imagens(nome_imagem)

        log.info("produto recebido com sucesso")

        return data["resultado"]

    # retorna todas as máquinas (id, loja, nome_imagem, modelo, visibilidade?)
    # se estiverem visíveis mostra.
    def requisita_todos_produtos(self):
        data = { "tipo_pedido" : "todos_produtos" }
        produtos = self.request(data)

        if not produtos or produtos.get("status") != 0 or "resultado" not in produtos:
            log.error("requisita_todos_produtos: resposta inválida")
            return { "status": -1, "resultado": [] }

        imagens_faltantes = get_imagens_faltantes(produtos)
        if imagens_faltantes:
            self.baixa_imagens(imagens_faltantes)

        log.info("Todas as imagens estão baixadas")
        return produtos

    # Retorna todas as informações sobre uma loja específica
    def requisita_loja(self, nome_loja):
        try:
            msg = { "tipo_pedido" : "requisita_loja", "nome" : nome_loja}
            loja = self.request(msg)
            # TODO converter dicionário em obj da classe Loja
            return loja
        except Exception as ex:
            log.error("erro em requisita loja")
            log.error(ex)

    # thread chama isso que coloca em static uma imagem
    def requisita_imagem(self, nome_imagem):
        # inicia uma nova conexão com o servidor
        # acho que se aproveitar o mesmo socket pode dar pau
        # então usa um socket auxiliar
        try:
            socket = JsonTSocket()
            log.info(f"Thread cliente conectando ao servidor {HOST}:{PORT}...")
            socket.connect(HOST, PORT)
        except Exception as e:
            log.error("Erro na conexão da thread cliente com o server")
            log.error(e)

        data = { "tipo_pedido" : "requisita_imagem",
                "imagem" : nome_imagem}

        socket.send_dict(data)

        # servidor devolve binário da imagem
        resposta = socket.recv_dict()

        # constrói imagem na pasta static
        imagem_conteudo = resposta["imagem_conteudo"]
        constroi_imagem(nome_imagem, imagem_conteudo)

        return

    def baixa_imagens(self, imagens_faltantes):
        """Busca imagens do servidor e baixa elas no cliente.
        não continua até todas as imagens estarem baixadas"""

        log.info(f"baixando imagens... {imagens_faltantes}")
        # requisita as imagens que não está em static em outras threads
        if isinstance(imagens_faltantes, list):
            try:
                treads = list()
                c = 0
                for imagem in imagens_faltantes:
                    treads.append(Thread(target=self.requisita_imagem,
                                         args=(imagem,)))
                    treads[c].start()
                    c+=1

                for tread in treads:
                    tread.join()
            except Exception as e:
                log.error("erro na criação das threads para "
                          "pegar as imagens")
                log.error(e)
        else:
            tread = Thread(target=self.requisita_imagem,
                           args=(imagens_faltantes,))
            tread.start()
            tread.join()

    def compra_produto(self, id):
        req = { "tipo_pedido" : "compra_produto", "id" : id }
        data = self.request(req)
        return data


# -------------- FUNÇÕES AUXILIARES -------------------------------------------

def busca_nome_imagem(data):
    return data["resultado"][0][3]

def constroi_imagem(nome_imagem, imagem_conteudo):
    try:
        with open(f"static/{nome_imagem}", 'wb') as f:
            f.write(base64.b64decode(imagem_conteudo))
    except Exception as e:
        log.error("erro na construção da imagem")
        log.error(e)
        exit(4)
    log.info(f"imagem {nome_imagem} construída com sucesso")

def get_imagens_dict(data):
    nomes_imagens = list()
    produtos = data["resultado"]
    for produto in produtos:
        nomes_imagens.append(produto[3])
    return nomes_imagens

def get_imagens_faltantes(data):
    imagens_cliente = os.listdir("static")
    imagens_banco = get_imagens_dict(data)
    imagens_faltantes = list()
    for imagem in imagens_banco:
        if imagem not in imagens_cliente:
            imagens_faltantes.append(imagem)
    return imagens_faltantes
