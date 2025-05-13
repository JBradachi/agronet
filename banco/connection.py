from threading import Thread
import socket
import sqlite3
import json
import logging as log

BUFSIZE = 4096

#TODO: coiso pra lidar com concorrencia
# (talvez fazer uma fila e executar cada Thread uma vez)
# "listener" não bloqueante joga as conexões numa fila
# executa uma thread por vez

class ConnectionHandler:
    def __init__(self, conn, addr):
        try:
            self.conn = conn
            self.addr_cliente = addr
            tread = Thread(target=self.run)
            tread.start()
        except:
            log.error("erro na criação da tread")
            exit(3)

    # Thread
    def run(self):
        try:
            log.info(f"Conexão recebida de {self.addr_cliente}")

            # A consulta, como descrito em docs/decisoes.md, é um JSON com dois
            # campos: um com a consulta em si e outro com seus parâmetros
            mensagem = self.conn.recv(BUFSIZE).decode()
            mensagem = json.loads(mensagem)
            # tenta executar a consulta
            try:
                conn_db = sqlite3.connect('./agronet.db')
                cursor = conn_db.cursor()
                try:
                    dados = cursor.execute(mensagem["consulta"],
                            tuple(mensagem["parametros"])).fetchall()
                except Exception as ex:
                    log.error(ex)
                    log.error("erro ao fazer a consulta")
                    log.error("pode ser a sintaxe")
                    exit(6)

                cursor.close()
            except:
                log.error("erro ao fazer a consulta")
                exit(4)

            # devolve a consulta em JSON
            dados_json = json.dumps(dados)
            self.conn.sendall(dados_json.encode())
            self.conn.close()
        except:
            log.error("erro na tread de resposta")
            exit(5)
