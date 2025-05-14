from dataclasses import dataclass, asdict

@dataclass
class Modelo:
    "Representação de um modelo de máquina"
    fabricante: str
    nome: str
    descricao: str

    def dict(self):
        return asdict(self)
