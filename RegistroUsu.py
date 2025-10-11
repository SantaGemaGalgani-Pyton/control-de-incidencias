import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro")
        self.setGeometry(100, 100, 500, 350)

        self.Ulabel = QLabel("Usuario")
        self.Clabel = QLabel("Contraseña")

        self.ISboton = QPushButton("Iniciar Sesión")
        self.ISboton.setFixedWidth(150)
        self.ISboton.setFixedHeight(35)

        self.Rboton = QPushButton("Registrarse")
        self.Rboton.setFixedWidth(150)
        self.Rboton.setFixedHeight(35)

        self.Utextarea = QLineEdit()

        self.Ctextarea = QLineEdit()
        self.Ctextarea.setEchoMode(QLineEdit.Password)

        self.ISboton.clicked.connect(self.iniciarsesion)
        self.Rboton.clicked.connect(self.registrarse)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.ISboton)
        layout_botones.addSpacing(20)
        layout_botones.addWidget(self.Rboton)
        layout_botones.addStretch()

        layout = QVBoxLayout()
        layout.addWidget(self.Ulabel)
        layout.addWidget(self.Utextarea)
        layout.addWidget(self.Clabel)
        layout.addWidget(self.Ctextarea)
        layout.addLayout(layout_botones)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

    def registrarse(self):
        # Alvaro base de datos ususario contraseña registro
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()

    def iniciarsesion(self):
        # Alvaro base de datos ususario contraseña comprobacion inicio sesion
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
