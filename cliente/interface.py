# Adiciona diretório pai ao path do python
# Para poder acessar a biblioteca protocolo
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget
from cliente import Cliente
from telas.login import TelaLogin
from telas.cadastro import TelaCadastro
from telas.mainScreen import TelaMainScreen
from telas.createShop import TelaCreateShop

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.cliente = Cliente()

        self.setWindowTitle("Cliente PyQt")
        self.setGeometry(100, 100, 300, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel("Digite seu nome:")
        self.layout.addWidget(self.label)

        self.input_nome = QLineEdit(self)
        self.layout.addWidget(self.input_nome)

        self.label = QLabel("Digite sua senha:")
        self.layout.addWidget(self.label)

        self.input_senha = QLineEdit(self)
        self.layout.addWidget(self.input_senha)

        self.botao = QPushButton("Enviar")
        self.botao.clicked.connect(self.enviar)
        self.layout.addWidget(self.botao)

        self.botao2 = QPushButton("testa_envio_produto")
        self.botao2.clicked.connect(self.envia_produto)
        self.layout.addWidget(self.botao2)

        self.botao3 = QPushButton("testa_recebimento_produto")
        self.botao3.clicked.connect(self.abre_produto)
        self.layout.addWidget(self.botao3)

        self.botao3 = QPushButton("testa_enviar_todos_produtos")
        self.botao3.clicked.connect(self.homepage)
        self.layout.addWidget(self.botao3)

        self.resposta_label = QLabel("")
        self.layout.addWidget(self.resposta_label)

        self.setLayout(self.layout)

    def enviar(self):
        nome = self.input_nome.text()
        senha = self.input_senha.text()
        if nome and senha:
            resposta = self.cliente.cadastra_usuario(nome, senha)
            self.resposta_label.setText(f"{resposta}")

    def envia_produto(self):
        resposta = self.cliente.insere_produto()
        self.resposta_label.setText(f"{resposta}")

    def abre_produto(self):
        resposta = self.cliente.requisita_produto_completo()
        self.resposta_label.setText(f"{resposta}")

    def homepage(self):
        resposta = self.cliente.requisita_todos_produtos()
        self.resposta_label.setText(f"{resposta}")

def main():
    app = QApplication(sys.argv)
    
    janela = Interface()
    janela.show()

    cliente = Cliente()
    stack = QStackedWidget()
    tela_login = TelaLogin(stack, cliente)
    tela_cadastro = TelaCadastro(stack, cliente)
    tela_main = TelaMainScreen(stack, cliente)
    tela_create_shop = TelaCreateShop(stack, cliente)

    stack.addWidget(tela_login)     # index 0
    stack.addWidget(tela_cadastro)  # index 1
    stack.addWidget(tela_main)      # index 2
    stack.addWidget(tela_create_shop)  # index 3 por exemplo
    
    stack.setWindowTitle("Cliente Distribuído")

    stack.setStyleSheet("""
        QWidget {
            background-color: white;
        }
        QLineEdit, QPushButton {
            background-color: white;
        }
    """)

    stack.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
