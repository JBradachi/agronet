import sqlite3
import logging as log
import base64
import Pyro5.api

@Pyro5.api.expose
class Banco:
    def __init__(self):
        try:
            conn_db = sqlite3.connect('./agronet.db')
            self.cursor = conn_db.cursor()
        except Exception as e:
            log.error("Erro ao gerar cursor do banco")
            log.error(e)

    def exec_query(self, msg):
        consulta = msg["consulta"]
        params = msg["parametros"]
        try:
            res = self.cursor.execute(consulta, params).fetchall()
            return {
                "status" : 0,
                "resultado" : res
            }
        except sqlite3.IntegrityError as ex:
            # Esse erro ocorre principalmente quando a chave primária do item
            # enviado colide com uma chave primária pré-existente
            log.error(ex)
            return {
                "status" : 1,
                "erro" : "integridade"
            }
        except Exception as ex:
            log.error("erro ao executar uma consulta (pode ser sintaxe)")
            log.error(ex)
            exit(6)

    def handle_insere_produto(self, msg):
        # verifica se existe imagem com o mesmo nome no banco
        try:
           msg = self.safe_name(msg)
        except Exception as e:
            log.error("erro ao tentar encontrar um nome seguro")
            log.error(e)

        resp = self.exec_query(msg)

        if resp["status"] != 0:
            return resp
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

        return { "status": 0 }

    def handle_requisita_imagem(self, msg):
        nome_imagem = msg["imagem"]
        resposta = { "status" : 0, }

        try:
            with open(f"static/{nome_imagem}", 'rb') as f:
                img_b64 = base64.b64encode(f.read()).decode('utf-8')
                resposta["imagem_conteudo"] = img_b64
        except Exception as e:
            log.error("erro na abertura do arquivo no envio")
            log.error(e)

        return resposta

    def handle_compra_produto(self, msg):
        id = msg["id"]
        # verifica se tem estoque
        verificacao = {
            "consulta" : "SELECT quantidade FROM Maquina WHERE id = ?",
            "parametros" : (id,) }
        resposta = self.exec_query(verificacao)
        quantidade = resposta["resultado"][0][0]

        if quantidade > 0:
            # compra bem sucedida, atualiza banco e retorna ok
            atualiza = {
                "consulta" : "UPDATE Maquina "
                "SET quantidade = quantidade - 1 "
                "WHERE id = ?",
                "parametros" : (id,)
            }
            self.exec_query(atualiza)
            return { "status" : 0,
                     "mensagem" : "compra bem sucedida"}

        # sem estoque
        return { "status" : -1,
                 "mensagem" : "compra mal sucedida, sem estoque"}

# --------------- AUXILIAR ---------------------

    def safe_name(self, msg):
            # tenta encontrar um nome que não de problemas
        while True:
            verificacao = { "consulta" : "SELECT imagem FROM Maquina "
                            "WHERE imagem = ?", "parametros": (msg['imagem'],)}
            existe = self.exec_query(verificacao)
            if not existe["resultado"]:
                break
            nome_atual = msg['imagem'].split(".")
            nome_atual[0] = nome_atual[0]+"-1"
            nome_novo = ".".join(nome_atual)
            msg['imagem'] = nome_novo
            msg["parametros"][0] = nome_novo

        return msg

daemon = Pyro5.server.Daemon()
ns = Pyro5.api.locate_ns()
uri = daemon.register(Banco)
ns.register("agronet.banco", uri)

log.info("Name server banco configurado")
daemon.requestLoop()
