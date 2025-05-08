from threading import Thread 
import socket
import sqlite3
import json
import logging as log

#TODO: coiso pra lidar com concorrencia 
# (talvez fazer uma fila e executar cada Thread uma vez)
# "listener" não bloqueante joga as conexões numa fila
# executa uma thread por vez

#TODO: trocar esse nome aqui pra deixar mais explicativo
class Connection:

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

            # recebe a consulta
            consulta = self.conn.recv(1024).decode()

            # tenta executar a consulta
            try:
                conn_db = sqlite3.connect('./agronet.db')
                cursor = conn_db.cursor()

                try:
                    dados = cursor.execute(consulta).fetchall()
                except:
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
