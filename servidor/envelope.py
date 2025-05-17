def consulta(sql, params):
    return {
        "tipo_consulta" : "padrao",
        "consulta" : sql,
        "parametros" : params
    }

def insere_produto(sql, params, base64_img, nome_imagem):
    return {
        "tipo_consulta" : "insere_produto",
        "consulta" : sql,
        "parametros" : params ,
        "imagem_conteudo" : base64_img,
        "imagem" : nome_imagem
    }

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
