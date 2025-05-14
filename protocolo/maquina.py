from dataclasses import dataclass, asdict

@dataclass
class Maquina:
    "Representação de uma máquina"
    loja: str
    modelo: int
    imagem: str
    preco: float
    mes_fabricacao: int
    ano_fabricacao: int
    visivel: bool
    id: int = -1 # desconhecido no momento do cadastro

    def dict(self):
        "Retorna o dicionário com todos os atributos"
        return asdict(self)

    def dict_cadastro(self):
        """
        Retorna o dicionário com todos os atributos, exceto aqueles que não
        são usados em um contexto de cadastro
        """
        data = asdict(self)
        del data["id"]
        return data
