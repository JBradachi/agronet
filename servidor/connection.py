from threading import Thread
import socket
import json
import logging as log

DB_HOST = "127.0.0.2"
DB_PORT = 3600

# TODO: acredito q agora é só da-lhe nos CSU
# usar esse protótipo pra fazer
class ConnectionHandler:

    # Passa para a thread informações necessárias e inicia
    def __init__(self, conn, addr):
        try:
            self.conn = conn
            self.addr_cliente = addr
            tread = Thread(target=self.run)
            tread.start()
        except:
            log.error("erro na criação da tread")
            exit(3)

    # Executa a thread
    def run(self):

        # cria uma conexão com o banco e executa a consulta
        try:
            #TODO: jogar tudo isso dentro de uma função
            conn_db = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            log.info("Thread conectando ao servidor"
                     f" de dados {DB_HOST}:{DB_PORT}...")

            conn_db.connect((DB_HOST, DB_PORT))

            # o banco recebe um JSON com a consulta e seus parâmetros
            consulta = "SELECT * FROM Usuario"
            mensagem = { "consulta" : consulta, "parametros" : []}
            mensagem = json.dumps(mensagem).encode()
            conn_db.sendall(mensagem)

            dados_json = conn_db.recv(1024).decode()
            dados = json.loads(dados_json)

            conn_db.close()

        except:
            log.error("erro ao contatar o servidor de dados")
            exit(4)

        # faz o envio dos dados para o cliente
        try:

            log.info(f"Conexão recebida de {self.addr_cliente}")

            nome = self.conn.recv(1024).decode()

            resposta = f"roi {nome}, né?{dados}"

            self.conn.sendall(resposta.encode())
            self.conn.close()
        except:
            log.error("erro na tread de resposta")
            exit(5)
