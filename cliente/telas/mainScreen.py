from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QFrame, QSizePolicy, QMessageBox
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
        pixmap = QPixmap(imagem_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
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

        self.setFixedSize(500, 350)

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
        carrossel_scroll.setFixedHeight(400)  # ou 330

        carrossel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        

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
        self.setStyleSheet("margin: 10px; padding: 10px; background-color: #f0f0f0; border-radius: 8px")


class TelaMainScreen(QWidget):  # <- Substitui QMainWindow por QWidget
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        print(cliente.requisita_todos_produtos())
        self.init_ui()

    def verifica_loja(self):
        nome_loja = self.cliente.usuario_logado["loja"]
        resposta = self.cliente.requisita_loja(nome_loja)

        if resposta.get("status") == 0:
            QMessageBox.information(self, "Minha Loja", f"A loja '{nome_loja}' já existe.")
            # self.stack.setCurrentIndex(?)  # redireciona para tela da loja
        else:
            self.stack.setCurrentIndex(3)  # redireciona para TelaCreateShop


    def init_ui(self):
        main_layout = QVBoxLayout()
        

        # Header
        header = QHBoxLayout()
        btn_inicio = QPushButton("Início")
        btn_loja = QPushButton("Minha Loja")
        btn_loja.clicked.connect(self.verifica_loja)

        header.addWidget(btn_inicio)
        header.addStretch()
        
        header.addWidget(btn_loja)

        header_widget = QWidget()
        header_widget.setFixedHeight(50)
        header_widget.setLayout(header)
        main_layout.addWidget(header_widget)

        # Scroll Area for Lojas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        scroll_container = QWidget()
        scroll_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        lojas_layout = QVBoxLayout()
        

        # Exemplo de dados
        resposta = self.cliente.requisita_todos_produtos()
        produtos_brutos = resposta.get("resultado", [])
        print(produtos_brutos)

        lojas_dict = {}
        
        for produto in produtos_brutos:
            id, loja_nome, modelo, nome_imagem, preco, quantidade = produto

            produto_info = {
                'nome': modelo,
                'preco': preco,
                'imagem': f'static/{nome_imagem}'
            }

            if loja_nome not in lojas_dict:
                lojas_dict[loja_nome] = []

            lojas_dict[loja_nome].append(produto_info)

        for loja_nome, produtos in lojas_dict.items():
            loja_widget = LojaWidget(loja_nome, produtos, self.abrir_pagina_produto)
            lojas_layout.addWidget(loja_widget)

        lojas_layout.addStretch()

        scroll_container.setLayout(lojas_layout)
        scroll_area.setWidget(scroll_container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def abrir_pagina_produto(self, nome_produto):
        print(f"Abrindo página para o produto: {nome_produto}")
