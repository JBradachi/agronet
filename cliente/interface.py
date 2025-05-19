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
from telas.myShop import TelaMinhaLoja
from telas.editProduct import TelaEditarProduto
from telas.createProduct import TelaCriarProduto
from telas.productDetail import TelaDetalheProduto


class Interface(QWidget):
    def __init__(self):
        super().__init__()

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

    cliente = Cliente()
    stack = QStackedWidget()
    tela_login = TelaLogin(stack, cliente)
    tela_cadastro = TelaCadastro(stack, cliente)
    tela_main = TelaMainScreen(stack, cliente)
    tela_create_shop = TelaCreateShop(stack, cliente)
    tela_minha_loja = TelaMinhaLoja(stack, cliente)
    tela_editar_produto = TelaEditarProduto(stack, cliente)
    tela_criar_produto = TelaCriarProduto(stack, cliente)
    tela_detalhe = TelaDetalheProduto(stack, cliente)

    stack.addWidget(tela_login)     # index 0
    stack.addWidget(tela_cadastro)  # index 1
    stack.addWidget(tela_main)      # index 2
    stack.addWidget(tela_create_shop)  # index 3 por exemplo
    stack.addWidget(tela_minha_loja)  # index 4
    stack.addWidget(tela_editar_produto)  # index 5
    stack.addWidget(tela_criar_produto)  # index 6
    stack.addWidget(tela_detalhe)  # index 7
    
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
