from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QMessageBox, QComboBox
)
import shutil
import os

class TelaCriarProduto(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.caminho_imagem = None

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Cadastrar Novo Produto"))

        self.input_modelo = QComboBox()
        self.input_modelo.addItems([
            "Challenger MT525D 4WD",
            "Escavadeira Hidráulica de Mineração 6015",
            "Semeadora Linha PLB",
            "Coffee Express Multi"
        ])
        self.input_modelo.setCurrentIndex(-1)  # Nenhum selecionado inicialmente
        layout.addWidget(self.input_modelo)


        self.input_preco = QLineEdit()
        self.input_preco.setPlaceholderText("Preço")
        layout.addWidget(self.input_preco)

        data_layout = QHBoxLayout()
        self.input_mes = QLineEdit()
        self.input_mes.setPlaceholderText("Mês")
        self.input_mes.setFixedWidth(50)
        data_layout.addWidget(self.input_mes)

        self.input_ano = QLineEdit()
        self.input_ano.setPlaceholderText("Ano")
        self.input_ano.setFixedWidth(70)
        data_layout.addWidget(self.input_ano)
        layout.addLayout(data_layout)

        self.input_quantidade = QLineEdit()
        self.input_quantidade.setPlaceholderText("Quantidade disponível")
        self.input_quantidade.setFixedWidth(70)
        data_layout.addWidget(self.input_quantidade)
        layout.addLayout(data_layout)

        self.btn_imagem = QPushButton("Selecionar Imagem")
        self.btn_imagem.clicked.connect(self.selecionar_imagem)
        layout.addWidget(self.btn_imagem)

        self.label_imagem = QLabel("Nenhuma imagem selecionada")
        layout.addWidget(self.label_imagem)

        self.btn_cadastrar = QPushButton("Cadastrar Produto")
        self.btn_cadastrar.clicked.connect(self.cadastrar)
        layout.addWidget(self.btn_cadastrar)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(lambda: self.stack.setCurrentIndex(4))  # TelaMinhaLoja
        layout.addWidget(self.btn_voltar)

        self.setLayout(layout)

    def selecionar_imagem(self):
        home_host = "/home/userhost"
        caminho, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Imagem",
            home_host,
            "Imagens (*.png *.jpg *.jpeg)"
        )

        if caminho:
            self.caminho_imagem = caminho
            self.label_imagem.setText(f"Imagem: {os.path.basename(caminho)}")

    def cadastrar(self):
        modelo = self.input_modelo.currentText()
        preco = self.input_preco.text()
        mes = self.input_mes.text()
        ano = self.input_ano.text()
        quantidade = self.input_quantidade.text()

        if not all([modelo, preco, mes, ano, self.caminho_imagem, quantidade]):
            QMessageBox.warning(self, "Erro", "Preencha todos os campos e selecione uma imagem.")
            return

        try:
            preco = float(preco)
            mes = int(mes)
            ano = int(ano)
            quantidade = int(quantidade)
        except:
            QMessageBox.warning(self, "Erro", "Preço, mês e ano devem ser numéricos.")
            return

        nome_imagem = os.path.basename(self.caminho_imagem)
        destino = os.path.join("static", nome_imagem)

        try:
            shutil.copy(self.caminho_imagem, destino)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao copiar imagem: {e}")
            return

        loja = self.cliente.usuario_logado["loja"]
        resposta = self.cliente.insere_produto(loja, modelo, preco, mes, ano, nome_imagem, quantidade)
        QMessageBox.information(self, "Status", str(resposta))
        self.stack.widget(2).carregar_dados()
        self.stack.widget(4).carregar_dados()
        self.stack.setCurrentIndex(4)
