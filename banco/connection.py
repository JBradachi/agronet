import base64
import sqlite3
import logging as log
from threading import Thread

from protocolo.protocolo import JsonTSocket

class ConnectionHandler:
    def __init__(self, conn: JsonTSocket, addr):
        # Inicializa dicionário de métodos
        self.handlers = {
            "padrao" : self.handle_padrao,
            "insere_imagem" : self.handle_insere_imagem,
        }

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
        while True:
            log.info(f"Conexão recebida de {self.addr_cliente}")

            # A mensagem recibida, no formato JsonT, possui três campos:
            # consulta, o SQL em si, parametros, que contém os parâmetros
            # da consulta, e tipo_consulta, cujo valor pode implicar a
            # existência de parâmetros adicionais
            try:
                msg = self.conn.recv_dict()
                if not msg: return # sem mensagem => encerramos
            except Exception as ex:
                log.info("erro na recepção da mensagem")
                log.info(ex)

            # Processamento da consulta
            try:
                handler = self.handlers.get(msg["tipo_consulta"], None)
                if not handler:
                    log.error("tipo de consulta não reconhecida")
                    log.error(msg["tipo_consulta"])
                    continue # próxima mensagem

                conn_db = sqlite3.connect('./agronet.db')
                self.cursor = conn_db.cursor()
                handler(msg)
                self.cursor.close()
                conn_db.commit()
            except Exception as ex:
                log.error("erro durante processamento básico")
                log.error(ex)
                exit(4)

# ------------------------------------------------------------------------------

    # Executa a consulta contida na mensagem, lidando com potenciais erros.
    # Retorna a resposta que deve ser dada, na forma de um dicionário python
    def exec_query(self, msg):
        consulta = msg["consulta"]
        params = msg["parametros"]
        try:
            res = self.cursor.execute(consulta, params).fetchall(),
            return {
                "status" : 0,
                "resultado" : res
            }
        except sqlite3.IntegrityError as ex:
            # Esse erro ocorre principalmente quando a chave primária do item
            # enviado colide com uma chave primária pré-existente
            log.info(ex)
            return {
                "status" : 1,
                "erro" : "integridade"
            }
        except Exception as ex:
            log.error("erro ao executar uma consulta (pode ser sintaxe)")
            log.error(ex)
            exit(6)

    def handle_padrao(self, msg):
        resp = self.exec_query(msg)
        self.conn.send_dict(resp)

    def handle_insere_imagem(self, msg):
        # verifica se existe imagem com o mesmo nome no banco
        msg = self.safe_name(msg)

        resp = self.exec_query(msg)
        if resp["status"] != 0:
            self.conn.send_dict(resp)
            return
        # Mensagens do desse tipo tem dois campos adicionais: 'imagem', que diz
        # o nome da mensagem sendo enviada, e 'imagem_conteudo', a imagem em si,
        # codificada em base 64
        try:
            nome_imagem = msg['imagem']
            imagem = msg['imagem_conteudo']
            with open(f"static/{nome_imagem}", 'wb') as f:
                f.write(base64.b64decode(imagem))
        except:
            log.error("erro no recebimento da imagem")
            exit(4)
        log.info("imagem inserida com sucesso")
        self.conn.send_dict(resp)

    def safe_name(self, msg):
        # tenta encontrar um nome que não de problemas
        while True:
            verificacao = { "consulta" : "SELECT imagem FROM Maquina WHERE imagem = ?",
            "parametros": (msg['imagem'],)}
            existe = self.exec_query(verificacao)
            if not existe["resultado"][0]:
                break
            nome_atual = msg['imagem'].split(".")
            nome_atual[0] = nome_atual[0]+"-1"
            nome_novo = ".".join(nome_atual)
            msg['imagem'] = nome_novo
            msg["parametros"][0] = nome_novo

        return msg
        
    