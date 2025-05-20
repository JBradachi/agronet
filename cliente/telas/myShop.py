from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os

class ProdutoCard(QWidget):
    def __init__(self, nome, preco, imagem_path, produto_id, on_editar_click):
        super().__init__()
        layout = QVBoxLayout()

        imagem = QLabel()
        if os.path.exists(imagem_path):
            pixmap = QPixmap(imagem_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
            imagem.setPixmap(pixmap)
        else:
            imagem.setText("Imagem não encontrada")

        imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(imagem)

        label_nome = QLabel(nome)
        label_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_nome)

        label_preco = QLabel(f"R$ {preco:.2f}")
        label_preco.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_preco)

        btn_editar = QPushButton("Editar")
        btn_editar.clicked.connect(lambda: on_editar_click(produto_id))  # aqui está a chave
        layout.addWidget(btn_editar)

        self.setLayout(layout)
        self.setFixedSize(300, 370)
        self.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")


class TelaMinhaLoja(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        self.header = self.criar_header()
        self.layout_principal.addWidget(self.header)

        btn_criar_produto = QPushButton("Criar Novo Produto")
        btn_criar_produto.clicked.connect(lambda: self.stack.setCurrentIndex(6))  # índice da nova tela
        self.layout_principal.addWidget(btn_criar_produto)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout_principal.addWidget(self.scroll_area)

    def criar_header(self):
        header = QHBoxLayout()
        btn_inicio = QPushButton("Início")
        btn_inicio.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        btn_loja = QPushButton("Minha Loja")
        header.addWidget(btn_inicio)
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        header.addWidget(btn_logout)
        header.addStretch()

        btn_ajuda = QPushButton("Ajuda")
        btn_ajuda.clicked.connect(self.ir_para_ajuda)
        header.addWidget(btn_ajuda)
        header.addWidget(btn_loja)

        header_widget = QWidget()
        header_widget.setFixedHeight(50)
        header_widget.setLayout(header)
        return header_widget

    def on_editar_click(self, id):
        tela_editar = self.stack.widget(5)  # índice da TelaEditarProduto
        tela_editar.carregar_produto(id)
        self.stack.setCurrentIndex(5)

    def carregar_dados(self):
        nome_loja = self.cliente.usuario_logado["loja"]
        resposta = self.cliente.requisita_todos_produtos()
        produtos = resposta.get("resultado", [])

        container = QWidget()
        layout_produtos = QHBoxLayout()

        for p in produtos:
            id, loja, modelo, nome_imagem, preco, visivel = p
            if loja == nome_loja:
                card = ProdutoCard(
                    modelo,
                    preco,
                    f"static/{nome_imagem}",
                    id,  # ID real do produto
                    self.on_editar_click
                )
                layout_produtos.addWidget(card)

        container.setLayout(layout_produtos)
        self.scroll_area.setWidget(container)

    def ir_para_ajuda(self):
        tela_ajuda = self.stack.widget(8)
        tela_ajuda.set_origem(self.stack.currentIndex())
        self.stack.setCurrentIndex(8)

    def logout(self):
        self.cliente.usuario_logado = None
        self.stack.setCurrentIndex(0)  # volta para tela de login
        self.stack.resize(350, 250)    # redimensiona para tela de login

