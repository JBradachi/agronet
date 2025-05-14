from dataclasses import dataclass, asdict

@dataclass
class Usuario: 
    nome: str
    senha: str
    loja: str

    def dict(self):
        return asdict(self)
