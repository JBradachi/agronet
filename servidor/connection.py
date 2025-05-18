import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from threading import Thread
import secrets, struct
import envelope
import logging as log
from protocolo.protocolo import JsonTSocket

DB_HOST = "127.0.0.2"
DB_PORT = 3600
PAYLOAD_SIZE = struct.calcsize("!Q")

# Classe que cria threads e lida com conexões
class ConnectionHandler:
    def __init__(self, conn: JsonTSocket, addr):

        # inicializa o dicionário de métodos
        self.handlers = {
            "login" : self.handle_login,
            "cadastra_usuario" : self.handle_cadastra_usuario,
            "cadastra_loja" : self.handle_cadastra_loja,
            "edita_produto" : self.handle_edita_produto,
            "cadastra_produto" : self.handle_cadastra_produto,
            "requisita_produto" : self.handle_requisita_produto,
            "todos_produtos" : self.handle_todos_produtos,
            "requisita_loja" : self.handle_requisita_loja,
            "requisita_imagem" : self.handle_requisita_imagem,
            "compra_produto" : self.handle_compra_produto,
        }

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
            self.setup_socket_db()
            while True:
                try:
                    pedido = self.conn.recv_dict()
                except Exception as e:
                    log.error("erro na decodificação do pedido")
                    log.error(e)

                if not pedido: break # conexão encerrada

                try:
                    handler = self.handlers.get(pedido["tipo_pedido"], None)
                    if not handler:
                        log.error("tipo de pedido não reconhecido")
                        log.error(pedido["tipo_pedido"])
                        continue # próxima mensagem
                    handler(pedido)
                except Exception as e:
                    log.info("falha no handler da thread servidor")
                    log.info(e)

        except Exception as e:
            log.error("erro ao executar a thread do servidor")
            log.error(e)
            exit(4) # não há como continuar

# ------------------------------------------------------------------------------

    # { "tipo_pedido" : "cadastra_usuario", "nome" : <nome>, "senha" : <senha> }
    def handle_cadastra_usuario(self, dados):
        nome = dados["nome"]
        senha = dados["senha"]
        # O usuário já existe no banco?
        msg = envelope.consulta(
                "SELECT * FROM Usuario "
                "WHERE nome = ?", (nome,))
        try:
            self.conn_db.send_dict(msg)
            resposta_db = self.conn_db.recv_dict()
            if not resposta_db or not resposta_db["resultado"]:
                # Esse aqui é caso que esperamos => usuário não existente
                # Cadastramos ele no banco de dado
                log.info("feito")
                msg = envelope.consulta(
                        "INSERT INTO Usuario (nome, senha) "
                        "VALUES (?, ?)", (nome, senha))
                try:
                    self.conn_db.send_dict(msg)
                    # A resposta não interessa muito aqui, creio eu
                    resposta_db = self.conn_db.recv_dict()
                except Exception as ex:
                    db_error()
                    log.error(ex)

                self.user = nome
                self.token = secrets.token_urlsafe(16)
                resposta = envelope.resposta_login(self.token, None)
            else:
                resposta = envelope.resposta_login(False)

            self.conn.send_dict(resposta)
        except Exception as ex:
            db_error()
            log.info(ex)

    # { "tipo_pedido" : "login", "nome" : <nome>, "senha" : <senha> }
    def handle_login(self, dados):
        nome = dados["nome"]
        senha = dados["senha"]
        # O usuário existe com essa senha no banco de dados?
        mensagem = envelope.consulta(
                "SELECT loja FROM Usuario "
                "WHERE nome = ? AND senha = ?", (nome, senha))
        try:
            self.conn_db.send_dict(mensagem)

            resposta_db = self.conn_db.recv_dict()
            #TODO: abubleblé
            if not resposta_db or not resposta_db["resultado"]:
                # sem resposta do banco => não existe tal usuário
                resposta = envelope.resposta_login(False)
            else:
                # Autentica o usuário nessa conexão
                self.token = secrets.token_urlsafe(16)
                self.user = nome
                self.loja = resposta_db["resultado"][0][0]
                resposta = envelope.resposta_login(self.token, self.loja)

            self.conn.send_dict(resposta)

        except Exception as e:
            db_error()
            log.info(e)

    # { "tipo_pedido" : "edita_produto", "id" : <id>, "visivel" : bool}
    def handle_edita_produto(self, dados):
        id_maquina = dados["id"]
        visivel = 1 if dados["visivel"] else 0
        mensagem = envelope.consulta("UPDATE Maquina SET visivel = ? WHERE id = ?", (id_maquina, visivel))
        log.info(f'A MENSAGEM: {mensagem}')
        try:
            log.info(f'A MENSAGEM: {mensagem}')
            resposta_db = self.conn_db.send_dict(mensagem)
            
            log.info(f"{resposta_db}")
            
            if resposta_db.get("status") != 0:
                self.conn.send_dict({"status": -1, "erro": "Erro ao atualizar visibilidade"})
            else:
                self.conn.send_dict(envelope.ok_resp())

        except Exception as e:
            log.error("Erro ao editar produto")
            log.error(e)
            self.conn.send_dict({"status": -1, "erro": "Exceção no servidor"})

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
        mensagem = envelope.consulta(
                "INSERT INTO Loja "
                "(nome, dia_criacao, mes_criacao, ano_criacao, "
                  "cidade, estado, descricao) VALUES "
                "(?, ?, ?, ?, ?, ?, ?)",
                (nome, dia_criacao, mes_criacao, ano_criacao,
                 cidade, estado, descricao))

        # Então, atualizamos o usuário atual com a chave estrangeira
        # referindo-se à loja
        mensagem2 = envelope.consulta(
                "UPDATE Usuario "
                "SET loja = ? "
                "WHERE nome = ?",
                (nome, self.user))

        try:
            self.conn_db.send_dict(mensagem)
            # Forte possibilidade de erro aqui: loja já existe
            resp_db = self.conn_db.recv_dict()

            if int(resp_db["status"]) != 0:
                # Erro: a loja já existe. Repassamos o erro para o cliente
                log.error("Erro!")
                self.conn.send_dict(resp_db)
                return

            self.conn_db.send_dict(mensagem2)
            self.conn_db.recv_dict()
            self.conn.send_dict(envelope.ok_resp())
        except: db_error()

    # { "tipo_pedido" : "cadastro_produto", dados_produto... }
    def handle_cadastra_produto(self, dados):
        # if not self.token:
        #     log.error("Usuário não logado, favor logar")
        #     return

        # if not self.loja:
        #     log.error("Usuário não possui loja")
        #     return
        modelo = dados["modelo"]
        preco = dados["preco"]
        mes_fabricacao = int(dados["mes_fabricacao"])
        ano_fabricacao = int(dados["ano_fabricacao"])
        nome_imagem = dados["imagem"]
        imagem_conteudo = dados["imagem_conteudo"]
        # loja = self.loja ? loja vai estar na conexão já
        loja = dados["loja"]

        params = [nome_imagem, loja, modelo, preco,
                mes_fabricacao, ano_fabricacao]

        mensagem = envelope.insere_produto(
            "INSERT INTO Maquina "
            "(imagem, loja, modelo, preco, mes_fabricacao, ano_fabricacao) "
            "VALUES (?, ?, ?, ?, ?, ?)", params, imagem_conteudo, nome_imagem)

        try:
            # tenta inserir os dados
            self.conn_db.send_dict(mensagem)
        except:
            log.error("erro na comunicação com o servidor de dados")
            log.error("handle_cadastra_produto, inserção de dados no banco")
            exit(4)

        self.conn.send_dict(envelope.ok_resp())

    # { "tipo_pedido": "requisita_produto", dados_produto...}
    def handle_requisita_produto(self, dados):
        id_maquina = dados["id"]
        params = [id_maquina,]
        mensagem = envelope.consulta(
            "SELECT * "
            "FROM Maquina INNER JOIN Modelo "
            "ON Maquina.modelo = Modelo.nome "
            "WHERE id = ?", params)
        try:
            self.conn_db.send_dict(mensagem)
        except:
            log.error("erro na comunicação com o servidor de dados")
            log.error("handle_requisita_produto, inserção de dados no banco")
            exit(4)

        resposta = self.conn_db.recv_dict()
        self.conn.send_dict(resposta)

    # { "tipo_pedido" : "todos_produtos" }
    def handle_todos_produtos(self, dados):
        params = ()
        mensagem = envelope.consulta(
            "SELECT id, loja, modelo, imagem, preco, visivel "
            "FROM Maquina", params)

        self.conn_db.send_dict(mensagem)
        resposta = self.conn_db.recv_dict()
        self.conn.send_dict(resposta)

    # { "tipo_pedido" : "requisita_loja", "nome" : <nome> }
    def handle_requisita_loja(self, dados):
        nome = dados["nome"]
        msg = envelope.consulta(
                "SELECT * FROM Loja WHERE nome  = ?", (nome,))
        self.conn_db.send_dict(msg)
        resposta = self.conn_db.recv_dict()
        self.conn.send_dict(resposta)
        return

    def handle_requisita_imagem(self, dados):
        nome_imagem = dados["imagem"]

        mensagem = { "tipo_consulta" : "requisita_imagem",
                    "imagem" : nome_imagem }

        self.conn_db.send_dict(mensagem)
        resposta = self.conn_db.recv_dict()

        self.conn.send_dict(resposta)
        return

    def handle_compra_produto(self, dados):
        id = dados["id"]

        mensagem = { "tipo_consulta" : "compra_produto", "id" : id }
        self.conn_db.send_dict(mensagem)
        resposta = self.conn_db.recv_dict()

        self.conn.send_dict(resposta)
        return

# ------------------------------------------------------------------------------

def db_error():
    log.error("erro na comunicação com o servidor de dados")
    exit(4)
