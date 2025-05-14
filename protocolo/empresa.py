from dataclasses import dataclass, asdict

@dataclass
class Empresa:
    nome: str

    def dict(self):
        return asdict(self)