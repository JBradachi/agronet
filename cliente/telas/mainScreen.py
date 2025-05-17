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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(4)

        imagem = QLabel()
        pixmap = QPixmap(imagem_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio)
        imagem.setPixmap(pixmap)
        imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_nome = QLabel(nome)
        label_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_preco = QLabel(f"R$ {preco:.2f}")
        label_preco.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_nome_e_preco = QHBoxLayout()
        label_nome_e_preco.addWidget(label_nome)
        label_nome_e_preco.addWidget(label_preco)

        label_nome_e_preco_widget = QWidget()
        label_nome_e_preco_widget.setLayout(label_nome_e_preco)

        layout.addWidget(imagem)
        layout.addWidget(label_nome_e_preco_widget)
        self.setLayout(layout)

        self.setFixedSize(500, 200)

        self.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")

        # Permitir clique
        self.mousePressEvent = lambda event: on_click_callback(nome)


class LojaWidget(QFrame):
    def __init__(self, nome_loja, produtos, on_produto_click):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel(nome_loja)
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; padding: 4px;")
        layout.addWidget(titulo)

        carrossel_scroll = QScrollArea()
        carrossel_scroll.setWidgetResizable(True)
        carrossel_scroll.setFixedHeight(300)
        carrossel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        carrossel_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        carrossel_layout = QHBoxLayout()
        carrossel_layout.setContentsMargins(0, 0, 0, 0)
        carrossel_layout.setSpacing(10)

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
            },
            {
                'nome': 'Loja B',
                'produtos': [
                    {'nome': 'Produto 3', 'preco': 30.0, 'imagem': 'static/exemplo.png'},
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
