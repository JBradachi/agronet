from threading import Thread
import socket
import json
import logging as log
import secrets

DB_HOST = "127.0.0.2"
DB_PORT = 3600
BUFSIZE = 4096

def setup_database_connection():
    conn_db = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    log.info("Thread conectando ao servidor"
             f" de dados {DB_HOST}:{DB_PORT}...")
    conn_db.connect((DB_HOST, DB_PORT))
    return conn_db

def consulta_json(sql, params):
    consulta = { "tipo_consulta" : "padrao", "consulta" : sql, 
                "parametros" : params }
    return json.dumps(consulta).encode()

def insere_imagem_json(sql, params):
    consulta = { "tipo_consulta" : "insere_imagem", "consulta" : sql, 
                "parametros" : params }
    return json.dumps(consulta).encode()

def requisita_imagem_json(sql, params):
    consulta = { "tipo_consulta" : "requisita_produto", "consulta" : sql, 
                "parametros" : params }
    return json.dumps(consulta).encode()

def resposta_login_json(token):
    # token pode ser
    # - uma URL segura de 32 caracteres se sucesso no login
    # - valor false se falhou no login
    if token: resposta = { "token" : token , "status" : 0}
    else: resposta = { "status" : -1 , "erro" : "Falha no login" }
    return json.dumps(resposta).encode()

def ok_resp():
    resp = { "status" : 0 }
    return json.dumps(resp).encode()

# Classe que cria threads e lida com conexões
class ConnectionHandler:
    def __init__(self, conn, addr):
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

    def __del__(self):
        self.conn.close()

    # Executa a thread
    def run(self):
        try:
            self.conn_db = setup_database_connection()
            while True:
                try:
                    pedido_json = self.conn.recv(BUFSIZE).decode()
                except Exception as e:
                    log.error("erro na decodificação do pedido")
                    log.error(e)
                if not pedido_json:
                    break # conexão encerrada
                pedido = json.loads(pedido_json)
                # O campo 'tipo_pedido' diz-nos como lidar com o pedido recebido
                ok = True
                match pedido["tipo_pedido"]:
                    case "login":
                        ok = self.handle_login(pedido)
                        resposta = resposta_login_json(ok)
                        self.conn.sendall(resposta)
                    case "edita_produto":
                        ok = self.handle_edita_produto(pedido)
                        if ok: self.conn.sendall(ok_resp())
                    case "cadastro_produto":
                        ok = self.handle_produto(pedido)
                        if ok: self.conn.sendall(ok_resp())
                    case _:
                        log.error("tipo de pedido não reconhecido")
                if not ok:
                    # TODO responder ao cliente aqui
                    log.info("O pedido não foi bem sucedido")

            self.conn_db.close()
        except:
            log.error("erro ao contatar o servidor de dados")
            exit(4) # não há como continuar

    # { "tipo_pedido" : "login", "nome" : <nome>, "senha" : <senha> }
    def handle_login(self, dados):
        nome = dados["nome"]
        senha = dados["senha"]
        # O usuário existe com essa senha no banco de dados?
        mensagem = consulta_json(
                "SELECT loja FROM Usuario "
                "WHERE nome = ? AND senha = ?", (nome, senha))
        try:
            self.conn_db.sendall(mensagem)
            resposta_db_json = self.conn_db.recv(BUFSIZE).decode()
            resposta_db = json.loads(resposta_db_json)
            if not resposta_db:
                # sem resposta do banco => não existe tal usuário
                return False
            self.token = secrets.token_urlsafe(16)
            self.user = nome
            self.loja = resposta_db[0][0] # salva a loja do usuário
            return self.token # deu bom, retorna token!
        except:
            log.error("erro na comunicação com o servidor de dados")
            exit(4)

    # { "tipo_pedido" : "edita_produto", "id" : <id>, "visivel" : bool}
    def handle_edita_produto(self, dados):
        id_maquina = dados["id"]
        visivel = 1 if dados["visivel"] else 0
        mensagem = consulta_json(
                "UPDATE Maquina "
                "SET visivel = ? "
                "WHERE id = ?", (id_maquina, visivel))
        try:
            self.conn_db.sendall(mensagem)
            # Não acho que a resposta do banco interessa muito nesse caso,
            # então simplesmente não faço nada com ela
            self.conn_db.recv(BUFSIZE).decode()
            return True
        except:
            log.error("erro na comunicação com o servidor de dados")
            exit(4)



    # { "tipo_pedido" : "cadastro_produto", "modelo" : <modelo>, 
    # "preco" : <preco>, "mes_fabricacao" : <mes_fabricacao>,
    # "ano_fabricacao" : <ano_fabricacao>, "imagem" : <nome_imagem> }
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
        # loja = self.loja
        loja = "adminStore"
        
        params = (nome_imagem, loja, modelo, preco, 
                mes_fabricacao, ano_fabricacao)
        
        #TODO: função que verifica se existe imagem de nome igual 
        # e muda nome se tiver antes de mandar pro banco
        #TODO: self guardar a loja do usuário, (se tiver)
        #TODO: banco ter um tipo pedido tambem: recebe_imagem e consulta
        mensagem = insere_imagem_json(
            "INSERT INTO Maquina "
            "(imagem, loja, modelo, preco, mes_fabricacao, ano_fabricacao) "
            "VALUES (?, ?, ?, ?, ?, ?)", params)

        try:
            # tenta inserir os dados 
            self.conn_db.sendall(mensagem)
        except:
            log.error("erro na comunicação com o servidor de dados")
            log.error("handle_produto, inserção de dados no banco")
            exit(4)
        # se tudo certo, pede para o cliente enviar a imagem
        self.conn.sendall(ok_resp())

        # se consegue inserir recebe o binário da imagem 
        # e repassa para o servidor de dados
        ok = json.loads(self.conn_db.recv(BUFSIZE).decode())
        if ok:
            try:    
                while True:
                    bin_img = self.conn.recv(BUFSIZE)
                    if not bin_img:
                        break
                    self.conn_db.sendall(bin_img)
            except:
                log.error("erro no envio da imagem")
                exit(4)
        
        return True