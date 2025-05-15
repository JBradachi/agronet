def consulta(sql, params):
    consulta = { "tipo_consulta" : "padrao", "consulta" : sql,
                "parametros" : params
                }
    return consulta

def insere_produto(sql, params, base64_img, nome_imagem):
    consulta = { "tipo_consulta" : "insere_produto", "consulta" : sql,
                "parametros" : params , "imagem_conteudo" : base64_img,
                "imagem" : nome_imagem
                }
    return consulta

def req_produto_completo(sql, params):
    consulta = { "tipo_consulta" : "req_produto_completo", "consulta" : sql,
                "parametros" : params
                }
    return consulta

def resposta_login(token):
    # token pode ser
    # - uma URL segura de 32 caracteres se sucesso no login
    # - valor false se falhou no login
    if token:
        resposta = { "token" : token , "status" : 0}
        return resposta
    else:
        resposta = { "status" : -1 , "erro" : "Falha no login" }
        return resposta

def ok_resp():
    resposta = { "status" : 0 }
    return resposta