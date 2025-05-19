from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os

class TelaDetalheProduto(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.id_produto = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label_imagem = QLabel()
        self.label_imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_imagem)

        self.label_info = QLabel()
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label_info)

        self.btn_comprar = QPushButton("Comprar")
        self.btn_comprar.clicked.connect(self.comprar)
        self.layout.addWidget(self.btn_comprar)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.layout.addWidget(self.btn_voltar)

    def carregar_produto(self, id_produto):
        self.id_produto = id_produto
        produto = self.cliente.requisita_produto_completo(id_produto)[0]

        loja, modelo, imagem, preco, mes, ano, visivel, quantidade = (
            produto[1], produto[2], produto[3], produto[4],
            produto[5], produto[6], produto[7], produto[8]
        )

        caminho_img = f"static/{imagem}"
        if os.path.exists(caminho_img):
            pixmap = QPixmap(caminho_img).scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio)
            self.label_imagem.setPixmap(pixmap)
        else:
            self.label_imagem.setText("Imagem não encontrada")

        self.label_info.setText(
            f"<b>Modelo:</b> {modelo}<br>"
            f"<b>Loja:</b> {loja}<br>"
            f"<b>Preço:</b> R$ {preco:,.2f}<br>"
            f"<b>Fabricação:</b> {mes}/{ano}<br>"
            f"<b>Quantidade:</b> {quantidade}"
        )

        # Desabilita compra se for da própria loja
        loja_usuario = self.cliente.usuario_logado.get("loja")
        if loja_usuario == loja:
            self.btn_comprar.setEnabled(False)
            self.btn_comprar.setText("Não é possível comprar da própria loja")
        else:
            self.btn_comprar.setEnabled(True)
            self.btn_comprar.setText("Comprar")

    def comprar(self):
        resposta = self.cliente.compra_produto(self.id_produto)
        QMessageBox.information(self, "Compra", str(resposta))
        self.stack.widget(2).carregar_dados()
        self.stack.setCurrentIndex(2)
