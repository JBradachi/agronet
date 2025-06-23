import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import secrets
import envelope
import logging as log
import Pyro5.api

log.basicConfig(level=log.INFO)

@Pyro5.api.expose
class ServidorSD:
    def __init__(self):
        try:
            ns = Pyro5.api.locate_ns()
            uri = ns.lookup("agronet.banco")
            self.banco = Pyro5.api.Proxy(uri)
            log.info("Conexão com o banco via Pyro estabelecida.")
        except Exception as e:
            log.error("Não foi possível conectar ao servidor de banco via Pyro")
            log.error(e)
            exit(64)

    def cadastra_usuario(self, nome, senha):
        msg = envelope.consulta("SELECT * FROM Usuario WHERE nome = ?", (nome,))
        try:
            resposta_db = self.banco.exec_query(msg)

            if resposta_db and resposta_db["resultado"]:
                return envelope.resposta_login(False)

            msg_insert = envelope.consulta(
                "INSERT INTO Usuario (nome, senha) VALUES (?, ?)", (nome, senha)
            )
            self.banco.exec_query(msg_insert)
            self.token = secrets.token_urlsafe(16)
            return envelope.resposta_login(self.token, None)
        except Exception as e:
            db_error()
            log.info(e)
            return {"status": -1, "erro": str(e)}

    def login(self, nome, senha):
        try:
            mensagem = envelope.consulta(
                "SELECT loja FROM Usuario WHERE nome = ? AND senha = ?", (nome, senha)
            )
            resposta_db = self.banco.exec_query(mensagem)

            if not resposta_db or not resposta_db["resultado"]:
                return envelope.resposta_login(False, None)

            self.token = secrets.token_urlsafe(16)
            self.loja = resposta_db["resultado"][0][0]
            self.user = nome
            return envelope.resposta_login(self.token, self.loja)
        except Exception as e:
            db_error()
            log.info(e)
            return {"status": -1, "erro": str(e)}

    def edita_produto(self, id_maquina, visivel):
        visivel_flag = 1 if visivel else 0
        mensagem = envelope.consulta("UPDATE Maquina SET visivel = ? WHERE id = ?", (visivel_flag, id_maquina))
        try:
            resposta_db = self.banco.exec_query(mensagem)
            if resposta_db.get("status") != 0:
                return {"status": -1, "erro": "Erro ao atualizar visibilidade"}
            else:
                return envelope.ok_resp()
        except Exception as e:
            log.error(e)
            return {"status": -1, "erro": "Erro ao editar produto"}

    def cadastra_loja(self, loja_dict):
        nome = loja_dict["nome"]
        dia_criacao = int(loja_dict["dia_criacao"])
        mes_criacao = int(loja_dict["mes_criacao"])
        ano_criacao = int(loja_dict["ano_criacao"])
        cidade = loja_dict["cidade"]
        estado = loja_dict["estado"]
        descricao = loja_dict["descricao"]

        mensagem = envelope.consulta(
                "INSERT INTO Loja (nome, dia_criacao, mes_criacao, ano_criacao, cidade, estado, descricao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (nome, dia_criacao, mes_criacao, ano_criacao, cidade, estado, descricao)
            )

        msg_user = envelope.consulta(
            "UPDATE Usuario SET loja = ? WHERE nome = ?", (nome, self.user)
        )

        try:
            resp_db = self.banco.exec_query(mensagem)

            if int(resp_db.get("status", -1)) != 0:
                return resp_db  # Erro no insert da loja


            self.banco.exec_query(msg_user)

            return envelope.ok_resp()
        except Exception as e:
            db_error()
            return {"status": -1, "erro": str(e)}

    def cadastra_produto(self, produto_dict, imagem_base64):
        params = [
            produto_dict["imagem"],
            produto_dict["loja"],
            produto_dict["modelo"],
            produto_dict["preco"],
            int(produto_dict["mes_fabricacao"]),
            int(produto_dict["ano_fabricacao"]),
            produto_dict["quantidade"]
        ]

        mensagem = envelope.insere_produto(
            "INSERT INTO Maquina (imagem, loja, modelo, preco, mes_fabricacao, ano_fabricacao, quantidade) VALUES (?, ?, ?, ?, ?, ?, ?)",
            params,
            imagem_base64,
            produto_dict["imagem"]
        )

        try:

            self.banco.handle_insere_produto(mensagem)
            return envelope.ok_resp()
        except Exception as e:
            db_error()
            return {"status": -1, "erro": str(e)}

    def requisita_produto(self, id):
        mensagem = envelope.consulta(
                "SELECT * FROM Maquina INNER JOIN Modelo ON Maquina.modelo = Modelo.nome WHERE id = ?",
                (id,)
            )
        try:
            return self.banco.exec_query(mensagem)
        except Exception as e:
            log.error(e)
            return {"status": -1, "erro": str(e)}

    def todos_produtos(self):
        mensagem = envelope.consulta(
            "SELECT id, loja, modelo, imagem, preco, visivel FROM Maquina", ()
        )
        try:
            return self.banco.exec_query(mensagem)
        except Exception as e:
            db_error()
            return {"status": -1, "erro": str(e)}

    def requisita_loja(self, nome):
        msg = envelope.consulta(
            "SELECT * FROM Loja WHERE nome = ?", (nome,)
        )
        try:
            return self.banco.exec_query(msg)
        except Exception as e:
            db_error()
            return {"status": -1, "erro": str(e)}

    def requisita_imagem(self, nome_imagem):
        mensagem = {"tipo_consulta": "requisita_imagem", "imagem": nome_imagem}
        try:
            return self.banco.handle_requisita_imagem(mensagem)
        except Exception as e:
            log.error(e)
            return {"status": -1, "erro": "Erro ao requisitar imagem"}

    def compra_produto(self, id):
        mensagem = {"tipo_consulta": "compra_produto", "id": id}
        try:
            return self.banco.handle_compra_produto(mensagem)
        except Exception as e:
            log.error(e)
            return {"status": -1, "erro": str(e)}

def db_error():
    log.error("Erro de comunicação com o servidor de banco de dados")
    exit(4)
