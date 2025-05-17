from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

class TelaCadastro(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.setFixedSize(350, 250)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Cadastro de Usuário"))

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Novo nome de usuário")
        layout.addWidget(self.input_nome)

        self.input_senha = QLineEdit()
        self.input_senha.setPlaceholderText("Senha")
        self.input_senha.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_senha)

        self.input_confirma = QLineEdit()
        self.input_confirma.setPlaceholderText("Confirmar senha")
        self.input_confirma.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_confirma)

        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.clicked.connect(self.fazer_cadastro)
        layout.addWidget(self.btn_cadastrar)

        self.btn_voltar = QPushButton("Voltar para login")
        self.btn_voltar.clicked.connect(self.voltar_login)
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)
        

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
