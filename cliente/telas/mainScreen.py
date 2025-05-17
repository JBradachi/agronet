from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ProdutoCard(QWidget):
    def __init__(self, nome, preco, imagem_path, on_click_callback):
        super().__init__()
        layout = QVBoxLayout()
        imagem = QLabel()
        pixmap = QPixmap(imagem_path).scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        imagem.setPixmap(pixmap)
        imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_nome = QLabel(nome)
        label_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_preco = QLabel(f"R$ {preco:.2f}")
        label_preco.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(imagem)
        layout.addWidget(label_nome)
        layout.addWidget(label_preco)
        self.setLayout(layout)

        # Permitir clique
        self.mousePressEvent = lambda event: on_click_callback(nome)


class LojaWidget(QFrame):
    def __init__(self, nome_loja, produtos, on_produto_click):
        super().__init__()
        layout = QVBoxLayout()
        titulo = QLabel(nome_loja)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold")
        layout.addWidget(titulo)

        carrossel_scroll = QScrollArea()
        carrossel_scroll.setWidgetResizable(True)
        carrossel_scroll.setFixedHeight(160)
        carrossel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        container = QWidget()
        carrossel_layout = QHBoxLayout()

        for produto in produtos:
            card = ProdutoCard(produto['nome'], produto['preco'], produto['imagem'], on_produto_click)
            carrossel_layout.addWidget(card)

        container.setLayout(carrossel_layout)
        carrossel_scroll.setWidget(container)
        layout.addWidget(carrossel_scroll)

        self.setLayout(layout)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 8px")


class TelaMainScreen(QWidget):  # <- Substitui QMainWindow por QWidget
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Header
        header = QHBoxLayout()
        btn_inicio = QPushButton("Início")
        btn_loja = QPushButton("Minha Loja")
        header.addWidget(btn_inicio)
        header.addStretch()
        header.addWidget(btn_loja)

        main_layout.addLayout(header)

        # Scroll Area for Lojas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        lojas_layout = QVBoxLayout()

        # Exemplo de dados
        lojas = [
            {
                'nome': 'Loja A',
                'produtos': [
                    {'nome': 'Produto 1', 'preco': 10.0, 'imagem': 'static/exemplo.png'},
                    {'nome': 'Produto 2', 'preco': 20.0, 'imagem': 'static/exemplo.png'},
                ]
            },
            {
                'nome': 'Loja B',
                'produtos': [
                    {'nome': 'Produto 3', 'preco': 30.0, 'imagem': 'static/exemplo.png'},
                ]
            }
        ]

        for loja in lojas:
            loja_widget = LojaWidget(loja['nome'], loja['produtos'], self.abrir_pagina_produto)
            lojas_layout.addWidget(loja_widget)

        scroll_container.setLayout(lojas_layout)
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def abrir_pagina_produto(self, nome_produto):
        print(f"Abrindo página para o produto: {nome_produto}")
