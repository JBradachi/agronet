import base64
from threading import Thread
import socket
import sqlite3
import json
import logging as log
import struct

BUFSIZE = 8192
PAYLOAD_SIZE = struct.calcsize("Q")

#TODO: coiso pra lidar com concorrencia
# (talvez fazer uma fila e executar cada Thread uma vez)
# "listener" não bloqueante joga as conexões numa fila
# executa uma thread por vez

def devolve_consulta(resposta):
    res_json = json.dumps(resposta).encode()
    tamanho_msg = struct.pack("Q", len(res_json)) 
    
    frame = tamanho_msg+res_json
    return frame

def ok_resp():
    resp = { "status" : 0 }
    return json.dumps(resp).encode()

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
            try:
                msg_size = self.conn.recv(PAYLOAD_SIZE)
                msg_size = struct.unpack("Q", msg_size)[0]
                mensagem = self.conn.recv(msg_size).decode()
                mensagem = json.loads(mensagem)
            except Exception as e:
                log.info("erro na decodificação da mensagem")
                log.info(e)
            # tenta executar a consulta
            try:
                conn_db = sqlite3.connect('./agronet.db')
                self.cursor = conn_db.cursor()
                match mensagem["tipo_consulta"]:
                    case "padrao":
                        dados = self.handle_padrao(mensagem)
                    case "insere_imagem":
                        dados = self.handle_insere_imagem(mensagem, conn_db)
                    case "requisita_produto":
                        pass
                    case _:
                        log.error("tipo de consulta não reconhecida")
                self.cursor.close()
            except:
                log.error("erro ao fazer a consulta")
                exit(4)

            # devolve a consulta em JSON
            try:
                self.conn.sendall(devolve_consulta(dados))
                self.conn.close()
            except Exception as e:
                log.info("Erro ao devolver a consulta JSON")
                log.info(e)

        except Exception as e:
            log.error("erro na tread de resposta")
            log.error(e)
            exit(5)

    def handle_padrao(self, mensagem):
        try:
            dados = self.cursor.execute(mensagem["consulta"],
                            tuple(mensagem["parametros"])).fetchall()
            return dados
        except Exception as ex:
            log.error(ex)
            log.error("erro ao fazer a consulta")
            log.error("pode ser a sintaxe")
            exit(6)

    def handle_insere_imagem(self, mensagem, conn_db:sqlite3.Connection):
        try:
            self.cursor.execute(mensagem["consulta"],
                            tuple(mensagem["parametros"])).fetchall()
        except Exception as e:
            log.error(e)
            log.error("erro ao fazer a consulta")
            log.error("pode ser a sintaxe")
            exit(6)

        try:
            with open(f"static/{mensagem['nome_imagem']}", 'wb') as f:
                f.write(base64.b64decode(mensagem['imagem']))
        except:
            log.error("erro no recebimento da imagem")
            exit(4)
        log.info("Enviou a imagem")
        conn_db.commit()
        return True