import json
import base64
import sqlite3
import logging as log
from threading import Thread

BUFSIZE = 8192

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

    def send_as_json(self, msg):
        try:
            if "status" not in msg:
                msg["status"] = 0 # assume que é ok
            msg_json = json.dumps(msg)
            self.conn.sendall(msg_json.encode())
            self.conn.close()
        except Exception as e:
            log.info("Erro ao devolver a consulta JSON")
            log.info(e)

    # Thread
    def run(self):
        try:
            log.info(f"Conexão recebida de {self.addr_cliente}")
            # A consulta em si é um JSON com três campos: consulta, o SQL em si,
            # parametros, que contém os parâmetros da consulta, e tipo_mensagem,
            # cujo valor pode implicar a existência de campos adicionais
            try:
                mensagem = self.conn.recv(BUFSIZE).decode()
                mensagem = json.loads(mensagem)
            except Exception as e:
                log.info("Erro na decodificação da mensagem")
                log.info(e)
            # tenta executar a consulta
            try:
                conn_db = sqlite3.connect('./agronet.db')
                self.cursor = conn_db.cursor()
                match mensagem["tipo_consulta"]:
                    case "padrao":
                        dados = self.handle_padrao(mensagem)
                        self.send_as_json(dados)
                    case "insere_imagem":
                        dados = self.handle_insere_imagem(mensagem)
                        conn_db.commit()
                        self.send_as_json(dados)
                    case "requisita_produto":
                        pass
                    case _:
                        log.error("tipo de consulta não reconhecida")
                self.cursor.close()
            except:
                log.error("erro ao fazer a consulta")
                exit(4)

        except Exception as e:
            log.error("erro na thread de resposta")
            log.error(e)
            exit(5)

# ------------------------------------------------------------------------------

    # Executa a consulta contida na mensagem, lidando com potenciais erros.
    # Retorna a resposta que deve ser dada, na forma de um dicionário python
    def exec_query(self, mensagem):
        consulta = mensagem["consulta"]
        params = mensagem["parametros"]
        try:
            res = self.cursor.execute(consulta, params).fetchall(),
            return {
                "status" : 0,
                "resultado" : res
            }
        except sqlite3.IntegrityError:
            # Esse erro ocorre principalmente quando a chave primária do item
            # enviado colide com uma chave primária pré-existente
            return {
                "status" : -1,
                "erro" : "integridade"
            }
        except Exception as ex:
            log.error(ex)
            log.error("erro ao fazer a consulta")
            log.error("pode ser a sintaxe")
            exit(6)

    def handle_padrao(self, mensagem):
        return self.exec_query(mensagem)

    def handle_insere_imagem(self, mensagem):
        dados = self.exec_query(mensagem)
        try:
            with open(f"static/{mensagem['nome_imagem']}", 'wb') as f:
                f.write(base64.b64decode(mensagem['imagem']))
        except:
            log.error("erro no recebimento da imagem")
            exit(4)
        log.info("Enviou a imagem")
        return dados
