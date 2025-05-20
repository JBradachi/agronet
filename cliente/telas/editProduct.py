from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import logging as log

class TelaEditarProduto(QWidget):
    def __init__(self, stack, cliente):
        super().__init__()
        self.stack = stack
        self.cliente = cliente
        self.produto = None
        self.setLayout(QVBoxLayout())

        self.label_titulo = QLabel("Editar Produto")
        self.layout().addWidget(self.label_titulo)

        self.imagem = QLabel()
        self.layout().addWidget(self.imagem)

        self.info = QLabel()
        self.layout().addWidget(self.info)

        self.check_visivel = QCheckBox("Produto visível na loja")
        self.layout().addWidget(self.check_visivel)

        self.btn_salvar = QPushButton("Salvar")
        self.btn_salvar.clicked.connect(self.salvar)
        self.layout().addWidget(self.btn_salvar)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self.voltar)
        self.layout().addWidget(self.btn_voltar)

    def carregar_produto(self, id_produto):
        resultado = self.cliente.requisita_produto_completo(id_produto)
        try:
            

            if not resultado or not isinstance(resultado, list) or not resultado[0]:
                raise ValueError("Produto não encontrado no servidor.")

            dados = resultado[0]
            log.info(f'RESULTADO: {resultado}')
            log.info(f'DADOS: {dados}')

            self.produto = {
                "id": id_produto,
                "id": dados[0],
                "modelo": dados[2],
                "imagem": f"static/{dados[3]}",
                "preco": dados[4],
                "visivel": bool(dados[7])
            }

            imagem_path = self.produto["imagem"]
            if os.path.exists(imagem_path):
                pixmap = QPixmap(imagem_path).scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
                self.imagem.setPixmap(pixmap)
            else:
                self.imagem.setText("Imagem não encontrada")

            self.info.setText(
                f"Modelo: {self.produto['modelo']}\nPreço: R$ {self.produto['preco']:.2f}"
            )
            self.check_visivel.setChecked(self.produto["visivel"])

        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao carregar produto: {e} {resultado}")

    def salvar(self):
        if not self.produto:
            QMessageBox.warning(self, "Erro", "Nenhum produto carregado.")
            return

        novo_valor = self.check_visivel.isChecked()
        resposta = self.cliente.edita_produto(self.produto["id"], novo_valor)

        QMessageBox.information(self, "Status", str(resposta))
        self.stack.widget(2).carregar_dados()
        self.stack.widget(4).carregar_dados()
        self.stack.setCurrentIndex(4)


    def voltar(self):
        self.stack.setCurrentIndex(4)
