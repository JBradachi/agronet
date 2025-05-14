from dataclasses import dataclass, asdict

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
    
    
