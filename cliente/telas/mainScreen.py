from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QPushButton, QLabel, QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap


class ProdutoCard(QWidget):
    def __init__(self, product_id, nome, preco, imagem_path, on_click_callback):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        imagem = QLabel()
        pixmap = QPixmap(imagem_path).scaled(220, 220, Qt.AspectRatioMode.KeepAspectRatio)
        imagem.setPixmap(pixmap)
        imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(imagem)

        label_nome = QLabel(nome)
        nomeCut = nome
        if len(nome) > 25:
            nomeCut = nome[:24] + "..."
        label_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_nome.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            padding: 2px;
            white-space: nowrap;
        """)
        label_nome.setToolTip(nome) # hover do nome
        label_nome.setText(nomeCut)
        layout.addWidget(label_nome)

        label_preco = QLabel(f"R$ {preco:,.2f}")
        label_preco.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_preco.setStyleSheet("color: green; font-size: 13px;")
        layout.addWidget(label_preco)

        self.setLayout(layout)
        self.setFixedSize(250, 320)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setStyleSheet("background-color: #fff; border: 1px solid #ccc; border-radius: 8px; ")

        self.mousePressEvent = lambda event: on_click_callback(product_id)

class LojaWidget(QFrame):
    def __init__(self, nome_loja, produtos, on_produto_click):
        super().__init__()
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        titulo = QLabel(nome_loja)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        grid_container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        # AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH NAO FUNCIONA
        grid_layout.setContentsMargins(10, 0, 10, 0)

        row = 0
        col = 0
        for produto in produtos:
            if produto["visibilidade"] == 0:
                continue

            card = ProdutoCard(
                produto["id"],
                produto["nome"],
                produto["preco"],
                produto["imagem"],
                on_produto_click
            )

            grid_layout.addWidget(card, row, col)

            col += 1
            if col >= 3:
                col = 0
                row += 1

        grid_container.setLayout(grid_layout)
        layout.addWidget(grid_container)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8f8f8; border-radius: 10px; margin-bottom: 16px;")



class TelaMainScreen(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente

        self.layout_principal = QVBoxLayout()
        self.setLayout(self.layout_principal)

        self.header = self.criar_header()
        self.layout_principal.addWidget(self.header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        # AAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAHAAHAHAH
        self.layout_principal.addWidget(self.scroll_area)

        self.scroll_container = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_container.setLayout(self.scroll_layout)

        self.scroll_area.setWidget(self.scroll_container)

        self.carregar_dados()

    def criar_header(self):
        header_layout = QHBoxLayout()
        btn_inicio = QPushButton("Início")
        btn_loja = QPushButton("Minha Loja")
        btn_loja.clicked.connect(self.verifica_loja)

        btn_ajuda = QPushButton("Ajuda")
        btn_ajuda.clicked.connect(self.ir_para_ajuda)

        header_layout.addWidget(btn_inicio)
        btn_logout = QPushButton("Logout")
        btn_logout.clicked.connect(self.logout)
        header_layout.addWidget(btn_logout)
        header_layout.addStretch()
        header_layout.addWidget(btn_ajuda)
        header_layout.addWidget(btn_loja)
        

        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setFixedHeight(50)
        return header_widget

    def carregar_dados(self):
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        resposta = self.cliente.requisita_todos_produtos()
        produtos = resposta.get("resultado", [])

        lojas_dict = {}

        for produto in produtos:
            id, loja_nome, modelo, nome_imagem, preco, visibilidade = produto

            info = {
                "id": id,
                "nome": modelo,
                "preco": preco,
                "imagem": f"static/{nome_imagem}",
                "visibilidade": visibilidade
            }

            lojas_dict.setdefault(loja_nome, []).append(info)

        for loja_nome, produtos in lojas_dict.items():
            loja_widget = LojaWidget(loja_nome, produtos, self.abrir_pagina_produto)
            self.scroll_layout.addWidget(loja_widget)

        self.scroll_layout.addStretch()

    def verifica_loja(self):
        loja = self.cliente.usuario_logado.get("loja")
        if loja:
            self.stack.widget(4).carregar_dados()
            self.stack.setCurrentIndex(4)
        else:
            self.stack.setCurrentIndex(3)

    def abrir_pagina_produto(self, product_id):
        
        self.stack.widget(7).carregar_produto(product_id)
        self.stack.setCurrentIndex(7)
        
    def ir_para_ajuda(self):
        tela_ajuda = self.stack.widget(8)
        tela_ajuda.set_origem(self.stack.currentIndex())
        self.stack.setCurrentIndex(8)

    def logout(self):
        self.cliente.usuario_logado = None
        self.stack.setCurrentIndex(0)  
        self.stack.resize(350, 250)   


