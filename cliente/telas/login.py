from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class TelaLogin(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.setFixedSize(350, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        caminho_logo = os.path.join("static", "agronetlogo.jpeg")
        if os.path.exists(caminho_logo):
            pixmap = QPixmap(caminho_logo).scaledToWidth(150)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            layout.addWidget(logo)

        layout.addWidget(QLabel("Login"))

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome de usuário")
        layout.addWidget(self.input_nome)

        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_senha)

        self.btn_login = QPushButton("Entrar")
        self.btn_login.clicked.connect(self.fazer_login)
        layout.addWidget(self.btn_login)

        self.btn_ir_para_cadastro = QPushButton("Não tem conta? Cadastre-se")
        self.btn_ir_para_cadastro.clicked.connect(self.ir_para_cadastro)
        layout.addWidget(self.btn_ir_para_cadastro)

        self.setLayout(layout)

        

    def fazer_login(self):
        nome = self.input_nome.text()
        senha = self.input_senha.text()

        if nome and senha:
            resposta = self.cliente.login(nome, senha)
            QMessageBox.information(self, "Resposta", str(resposta))
        else:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if resposta.get("status") == 0:
            self.stack.setCurrentIndex(2)
            self.stack.resize(1080,720)
            


    def ir_para_cadastro(self):
        self.stack.setCurrentIndex(1)
