# Adiciona diretório pai ao path do python
# Para poder acessar a biblioteca protocolo
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import base64
import logging as log

import Pyro5.api
from protocolo.protocolo import JsonTSocket
from protocolo.entidades import Loja, Usuario, Maquina
from threading import Thread

HOST = "127.0.0.1"
PORT = 6000

log.basicConfig(level=log.INFO)

class Cliente:
    def __init__(self):
        try:
            ns = Pyro5.api.locate_ns()
            uri = ns.lookup("agronet.aplicacao")
            self.server = Pyro5.api.Proxy(uri)
            log.info("Conectado ao servidor de aplicação via Pyro.")
        except Exception as e:
            log.error("Erro ao conectar ao servidor de aplicação via Pyro")
            log.error(e)
            exit(64)
        self.usuario_logado = None

    def login(self, nome, senha):
        usuario = Usuario(nome, senha)
        data = usuario.dict()
        data["tipo_pedido"] = "login"
        resposta = self.server.login(nome, senha) # mudar para usar Usuario na chamada

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
        return self.server.cadastra_usuario(nome, senha) # mudar para usar Usuario na chamada

    def cadastra_loja(self, nome, dia_criacao, mes_criacao, ano_criacao,
        cidade, estado, descricao):
        loja = Loja(nome, dia_criacao, mes_criacao, ano_criacao,
            cidade, estado, descricao)
        dados = loja.dict()
        return self.server.cadastra_loja(dados)

    def edita_produto(self, id, visivel):
        log.info(f"MUDANÇA DE VISIBILIDADE ID: {id} VISIB: {visivel}")
        return self.server.edita_produto(id, visivel)

    # TODO: na integração add os parametros
    # loja, modelo, preco, mes_fabricacao, ano_fabricacao, nome_imagem
    def insere_produto(self, loja, modelo, preco, mes_fabricacao, ano_fabricacao, nome_imagem, quantidade):
        produto = Maquina(loja, modelo, nome_imagem, preco, mes_fabricacao, ano_fabricacao, True, quantidade)
        data = produto.dict()

        try:
            with open(f"static/{produto.imagem}", 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
            return self.server.cadastra_produto(data, img_b64)
        except Exception as e:
            log.error(e)
            log.error("falha em insere_produto")


    # a partir de um id de máquina, retorna todas as info delas
    # em um dicionário
    # TODO: na integração adicionar id como parametro
    def requisita_produto_completo(self, id):
        resposta = self.server.requisita_produto(id)

        nome_imagem = busca_nome_imagem(resposta)
        if nome_imagem not in os.listdir("static"):
            self.baixa_imagens(nome_imagem)

        log.info("produto recebido com sucesso")

        return resposta["resultado"]

    # retorna todas as máquinas (id, loja, nome_imagem, modelo, visibilidade?)
    # se estiverem visíveis mostra.
    def requisita_todos_produtos(self):
        produtos = self.server.todos_produtos()

        if not produtos or produtos.get("status") != 0 or "resultado" not in produtos:
            log.error("requisita_todos_produtos: resposta inválida")
            return { "status": -1, "resultado": [] }

        imagens_faltantes = self.get_imagens_faltantes(produtos)
        if imagens_faltantes:
            self.baixa_imagens(imagens_faltantes)

        log.info("Todas as imagens estão baixadas")
        return produtos

    # Retorna todas as informações sobre uma loja específica
    def requisita_loja(self, nome_loja):
        try:
            return self.server.requisita_loja(nome_loja)
        except Exception as ex:
            log.error("erro em requisita loja")
            log.error(ex)

    # thread chama isso que coloca em static uma imagem
    def requisita_imagem(self, nome_imagem):
        # inicia uma nova conexão com o servidor
        # acho que se aproveitar o mesmo socket pode dar pau
        # então usa um socket auxiliar
        try:
            resposta = self.server.requisita_imagem(nome_imagem)
            self.constroi_imagem(nome_imagem, resposta["imagem_conteudo"])
        except Exception as e:
            log.error("Erro ao requisitar imagem via Pyro")
            log.error(e)

    def baixa_imagens(self, imagens_faltantes):
        """Busca imagens do servidor e baixa elas no cliente.
        não continua até todas as imagens estarem baixadas"""

        log.info(f"baixando imagens... {imagens_faltantes}")
        # requisita as imagens que não está em static em outras threads
        threads = []
        if isinstance(imagens_faltantes, list):
            for imagem in imagens_faltantes:
                t = Thread(target=self.requisita_imagem, args=(imagem,))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
        else:
            self.requisita_imagem(imagens_faltantes)

    def compra_produto(self, id):
        return self.server.compra_produto(id)
    
    def get_imagens_faltantes(self, data):
        imagens_cliente = os.listdir("static")
        imagens_banco = [produto[3] for produto in data["resultado"]]
        return [img for img in imagens_banco if img not in imagens_cliente]

    def constroi_imagem(self, nome_imagem, imagem_conteudo):
        try:
            with open(f"static/{nome_imagem}", 'wb') as f:
                f.write(base64.b64decode(imagem_conteudo))
            log.info(f"Imagem {nome_imagem} salva com sucesso.")
        except Exception as e:
            log.error("Erro ao salvar imagem localmente.")
            log.error(e)


# -------------- FUNÇÕES AUXILIARES -------------------------------------------

def busca_nome_imagem(data):
    return data["resultado"][0][3]
