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
