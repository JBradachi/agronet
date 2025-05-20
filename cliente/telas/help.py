from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class TelaAjuda(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.origem = 0 
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        titulo = QLabel("Precisa de ajuda?")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(titulo)

        texto = QLabel(
            "Entre em contato com os desenvolvedores:\n\n"
            "Zezinho – a@gmail.com – +55 66 99999-9999\n"
            "Huguinho – b@gmail.com – +55 66 99999-9998\n"
            "Luisinho – c@gmail.com – +55 66 99999-9997"
        )
        texto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        texto.setWordWrap(True)
        layout.addWidget(texto)

        self.btn_voltar = QPushButton("Voltar")
        self.btn_voltar.clicked.connect(self.voltar)
        layout.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def set_origem(self, indice):
        self.origem = indice

    def voltar(self):
        self.stack.setCurrentIndex(self.origem)
