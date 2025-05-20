from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt

class TelaCadastro(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.init_ui()

    def init_ui(self):
        layout_externo = QVBoxLayout()
        layout_externo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        conteudo = QWidget()
        layout_conteudo = QVBoxLayout()
        layout_conteudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conteudo.setLayout(layout_conteudo)

        titulo = QLabel("Cadastro de Usuário")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_conteudo.addWidget(titulo)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Novo nome de usuário")
        layout_conteudo.addWidget(self.input_nome)

        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout_conteudo.addWidget(self.input_senha)

        self.input_confirma = QLineEdit()
        self.input_confirma.setPlaceholderText("Confirmar senha")
        self.input_confirma.setEchoMode(QLineEdit.EchoMode.Password)
        layout_conteudo.addWidget(self.input_confirma)

        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.clicked.connect(self.fazer_cadastro)
        layout_conteudo.addWidget(self.btn_cadastrar)

        self.btn_voltar = QPushButton("Voltar para login")
        self.btn_voltar.clicked.connect(self.voltar_login)
        layout_conteudo.addWidget(self.btn_voltar)

        layout_externo.addStretch()
        layout_externo.addWidget(conteudo)
        layout_externo.addStretch()

        self.setLayout(layout_externo)

    def fazer_cadastro(self):
        nome = self.input_nome.text()
        senha = self.input_senha.text()
        confirma = self.input_confirma.text()

        if not (nome and senha and confirma):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if senha != confirma:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem.")
            return

        resposta = self.cliente.cadastra_usuario(nome, senha)
        QMessageBox.information(self, "Cadastro", str(resposta))

    def voltar_login(self):
        self.stack.setCurrentIndex(0)
