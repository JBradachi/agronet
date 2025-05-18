from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from datetime import datetime

class TelaCreateShop(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.setFixedSize(400, 350)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Criar Nova Loja"))

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome da loja")
        layout.addWidget(self.input_nome)

        self.input_cidade = QLineEdit()
        self.input_cidade.setPlaceholderText("Cidade")
        layout.addWidget(self.input_cidade)

        self.input_estado = QLineEdit()
        self.input_estado.setPlaceholderText("Estado")
        layout.addWidget(self.input_estado)

        self.input_descricao = QLineEdit()
        self.input_descricao.setPlaceholderText("Descrição")
        layout.addWidget(self.input_descricao)

        self.btn_criar = QPushButton("Criar Loja")
        self.btn_criar.clicked.connect(self.criar_loja)
        layout.addWidget(self.btn_criar)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self.voltar)
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)

    def criar_loja(self):
        nome = self.input_nome.text()
        cidade = self.input_cidade.text()
        estado = self.input_estado.text()
        descricao = self.input_descricao.text()

        if not all([nome, cidade, estado, descricao]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        hoje = datetime.today()
        dia = hoje.day
        mes = hoje.month
        ano = hoje.year

        resposta = self.cliente.cadastra_loja(nome, dia, mes, ano, cidade, estado, descricao)
        QMessageBox.information(self, "Resultado", str(resposta))

    def voltar(self):
        self.stack.setCurrentIndex(2)  # Volta para a tela principal
