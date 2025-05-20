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
        self.init_ui()

    def init_ui(self):
        layout_externo = QVBoxLayout()
        layout_externo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Widget encapsulado com todo o conteúdo
        conteudo = QWidget()
        layout_conteudo = QVBoxLayout()
        layout_conteudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        conteudo.setLayout(layout_conteudo)

        # Logo
        caminho_logo = os.path.join("static", "agronetlogo.jpeg")
        if os.path.exists(caminho_logo):
            pixmap = QPixmap(caminho_logo).scaledToWidth(150)
            logo = QLabel()
            logo.setPixmap(pixmap)
            logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout_conteudo.addWidget(logo)

        # Título
        titulo = QLabel("Login")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_conteudo.addWidget(titulo)

        # Campo de nome
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome de usuário")
        layout_conteudo.addWidget(self.input_nome)

        # Campo de senha
        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout_conteudo.addWidget(self.input_senha)

        # Botões
        self.btn_login = QPushButton("Entrar")
        self.btn_login.clicked.connect(self.fazer_login)
        layout_conteudo.addWidget(self.btn_login)

        self.btn_ir_para_cadastro = QPushButton("Não tem conta? Cadastre-se")
        self.btn_ir_para_cadastro.clicked.connect(self.ir_para_cadastro)
        layout_conteudo.addWidget(self.btn_ir_para_cadastro)

        self.btn_ajuda = QPushButton("Ajuda")
        self.btn_ajuda.clicked.connect(self.ir_para_ajuda)
        layout_conteudo.addWidget(self.btn_ajuda)


        # Adiciona o conteúdo encapsulado ao layout externo
        layout_externo.addStretch()
        layout_externo.addWidget(conteudo)
        layout_externo.addStretch()

        self.setLayout(layout_externo)

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
            self.stack.resize(1080, 720)

    def ir_para_cadastro(self):
        self.stack.setCurrentIndex(1)

    def ir_para_ajuda(self):
        tela_ajuda = self.stack.widget(8)
        tela_ajuda.set_origem(self.stack.currentIndex())
        self.stack.setCurrentIndex(8)
