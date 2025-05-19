from dataclasses import dataclass, asdict

@dataclass
class Usuario:
    nome: str
    senha: str
    loja: str = ""

    def dict(self):
        data = asdict(self)
        if self.loja == "":
            del data["loja"]
        return data

@dataclass
class Empresa:
    nome: str

    def dict(self):
        return asdict(self)

@dataclass
class Loja:
    nome: str
    dia_criacao: int
    mes_criacao: int
    ano_criacao: int
    cidade: str
    estado: str
    descricao: str

    def dict(self):
        return asdict(self)

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
    quantidade: int
    id: int = -1 # desconhecido no momento do cadastro
    

    def dict(self):
        data = asdict(self)
        if self.id < 0:
            del data["id"]
        return data

@dataclass
class Modelo:
    "Representação de um modelo de máquina"
    fabricante: str
    nome: str
    descricao: str

    def dict(self):
        return asdict(self)
