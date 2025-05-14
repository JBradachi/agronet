import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from threading import Thread
import json, secrets, struct
import logging as log
from protocolo.protocolo import JsonTSocket

DB_HOST = "127.0.0.2"
DB_PORT = 3600
PAYLOAD_SIZE = struct.calcsize("!Q")

def monta_frame(dados):
    dados_bin = json.dumps(dados).encode()
    tamanho_msg = struct.pack("!Q", len(dados_bin))

    return tamanho_msg+dados_bin

def consulta_json(sql, params):
    consulta = { "tipo_consulta" : "padrao", "consulta" : sql,
                "parametros" : params
                }
    return consulta

def insere_imagem_json(sql, params, base64_img, nome_imagem):
    consulta = { "tipo_consulta" : "insere_imagem", "consulta" : sql,
                "parametros" : params , "imagem_conteudo" : base64_img,
                "imagem" : nome_imagem
                }
    return consulta

def requisita_imagem_json(sql, params):
    consulta = { "tipo_consulta" : "requisita_produto", "consulta" : sql,
                "parametros" : params
                }
    return consulta

def resposta_login(token):
    # token pode ser
    # - uma URL segura de 32 caracteres se sucesso no login
    # - valor false se falhou no login
    if token:
        resposta = { "token" : token , "status" : 0}
        return True, resposta
    else:
        resposta = { "status" : -1 , "erro" : "Falha no login" }
        return False, resposta

def ok_resp():
    resposta = { "status" : 0 }
    return resposta

def db_error():
    log.error("erro na comunicação com o servidor de dados")
    exit(4)

# Classe que cria threads e lida com conexões
class ConnectionHandler:
    def __init__(self, conn: JsonTSocket, addr):
        try:
            self.conn = conn
            self.addr_cliente = addr
            self.token = None
            self.user = ""
            tread = Thread(target=self.run)
            tread.start()
        except:
            log.error("erro na criação da tread")
            exit(3)

    def setup_socket_db(self):
        try:
            self.conn_db = JsonTSocket()
            log.info("Thread conectando ao servidor"
                    f" de dados {DB_HOST}:{DB_PORT}...")
            self.conn_db.connect(DB_HOST, DB_PORT)
        except Exception as e:
            log.error("Não foi possível conectar ao servidor de dados")
            log.error(e)
            exit(64)

    # Executa a thread
    def run(self):
        try:
            while True:
                self.setup_socket_db()
                try:
                    pedido = self.conn.recv_dict()
                except Exception as e:
                    log.error("erro na decodificação do pedido")
                    log.error(e)

                if not pedido:
                    break # conexão encerrada

                # O campo 'tipo_pedido' diz-nos como lidar com o pedido recebido
                ok = True
                match pedido["tipo_pedido"]:
                    case "login":
                        token = self.handle_login(pedido)
                        ok, resposta = resposta_login(token)
                        self.conn.send_dict(resposta)
                    case "cadastra_loja":
                        resposta = self.handle_cadastra_loja(pedido)
                        self.conn.send_dict(resposta)
                    case "edita_produto":
                        ok = self.handle_edita_produto(pedido)
                        if ok: self.conn.send_dict(ok_resp())
                    case "cadastro_produto":
                        ok = self.handle_produto(pedido)
                        if ok: self.conn.send_dict(ok_resp())
                    case _:
                        log.error("tipo de pedido não reconhecido")
                if not ok:
                    # TODO responder ao cliente aqui
                    log.info("O pedido não foi bem sucedido")
        except Exception as e:
            log.error("erro ao contatar o servidor de dados")
            log.error(e)
            exit(4) # não há como continuar

# ------------------------------------------------------------------------------

    # { "tipo_pedido" : "login", "nome" : <nome>, "senha" : <senha> }
    def handle_login(self, dados):
        nome = dados["nome"]
        senha = dados["senha"]
        # O usuário existe com essa senha no banco de dados?
        mensagem = consulta_json(
                "SELECT loja FROM Usuario "
                "WHERE nome = ? AND senha = ?", (nome, senha))
        try:
            self.conn_db.send_dict(mensagem)

            resposta_db = self.conn_db.recv_dict()
            #TODO: abubleblé 
            if not resposta_db or not resposta_db["resultado"][0]:
                # sem resposta do banco => não existe tal usuário
                return False
            self.token = secrets.token_urlsafe(16)
            self.user = nome
            # Alerta de linha absolutamente horrorosa abaixo
            self.loja = resposta_db["resultado"][0][0]
            return self.token # deu bom, retorna token!
        except Exception as e: 
            db_error()
            log.info(e)

    # { "tipo_pedido" : "edita_produto", "id" : <id>, "visivel" : bool}
    def handle_edita_produto(self, dados):
        id_maquina = dados["id"]
        visivel = 1 if dados["visivel"] else 0
        mensagem = consulta_json(
                "UPDATE Maquina "
                "SET visivel = ? "
                "WHERE id = ?", (id_maquina, visivel))
        try:
            self.conn_db.send_dict(mensagem)
            # Não acho que a resposta do banco interessa muito nesse caso,
            # então simplesmente não faço nada com ela
            self.conn_db.recv_dict()
            return True
        except: db_error()

    # { "tipo_pedido" : "cadastra_loja", dados_loja... }
    def handle_cadastra_loja(self, dados):
        nome = dados["nome"]
        dia_criacao = int(dados["dia_criacao"])
        mes_criacao = int(dados["mes_criacao"])
        ano_criacao = int(dados["ano_criacao"])
        cidade = dados["cidade"]
        estado = dados["estado"]
        descricao = dados["descricao"]

        # TODO verificar se o usuário já não tem uma loja
        # Primeiramente, adicionamos a loja em si no BD
        mensagem = consulta_json(
                "INSERT INTO Loja "
                "(nome, dia_criacao, mes_criacao, ano_criacao, "
                  "cidade, estado, descricao) VALUES "
                "(?, ?, ?, ?, ?, ?, ?)",
                (nome, dia_criacao, mes_criacao, ano_criacao,
                 cidade, estado, descricao))
        
        # Então, atualizamos o usuário atual com a chave estrangeira
        # referindo-se à loja
        mensagem2 = consulta_json(
                "UPDATE Usuario "
                "SET loja = ? "
                "WHERE nome = ?",
                (nome, self.user))

        try:
            self.conn_db.send_dict(mensagem)
            # Forte possibilidade de erro aqui: loja já existe
            resp_db = self.conn_db.recv_dict()

            if int(resp_db["status"]) != 0:
                # Erro: a loja já existe. Repassamos o erro para o servidor
                log.error("Erro!")
                return json.dumps(resp_db)

            self.conn_db.send_dict(mensagem2)
            self.conn_db.recv_dict()
            return ok_resp()
        except: db_error()

    # { "tipo_pedido" : "cadastro_produto", "modelo" : <modelo>,
    # "preco" : <preco>, "mes_fabricacao" : <mes_fabricacao>,
    # "ano_fabricacao" : <ano_fabricacao>, "imagem" : <nome_imagem>
    # "imagem_conteudo" : base64_img }
    def handle_produto(self, dados):
        # if not self.token:
        #     log.error("Usuário não logado, favor logar")
        #     return

        # if not self.loja:
        #     log.error("Usuário não possui loja")
        #     return
        modelo = dados["modelo"]
        preco = dados["preco"]
        mes_fabricacao = dados["mes_fabricacao"]
        ano_fabricacao = dados["ano_fabricacao"]
        nome_imagem = dados["imagem"]
        imagem_conteudo = dados["imagem_conteudo"]
        # loja = self.loja
        loja = dados["loja"]

        params = (nome_imagem, loja, modelo, preco,
                mes_fabricacao, ano_fabricacao)

        #TODO: função que verifica se existe imagem de nome igual
        # e muda nome se tiver antes de mandar pro banco
        #TODO: self guardar a loja do usuário, (se tiver)
        #TODO: banco ter um tipo pedido tambem: recebe_imagem e consulta
        mensagem = insere_imagem_json(
            "INSERT INTO Maquina "
            "(imagem, loja, modelo, preco, mes_fabricacao, ano_fabricacao) "
            "VALUES (?, ?, ?, ?, ?, ?)", params, imagem_conteudo, nome_imagem)

        try:
            # tenta inserir os dados
            self.conn_db.send_dict(mensagem)
        except:
            log.error("erro na comunicação com o servidor de dados")
            log.error("handle_produto, inserção de dados no banco")
            exit(4)

        return True
