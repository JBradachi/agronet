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
        data = asdict(self)
        if self.id < 0:
            del data["id"]
        return data
