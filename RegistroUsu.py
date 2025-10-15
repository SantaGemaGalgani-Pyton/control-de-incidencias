import sys
from bbdd import BaseDeDatos
from VentanaPrincipal import VentanaPrincipal as mainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class VentanaPrincipal(QWidget):
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd

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
        self.Usuario = self.Utextarea.text().strip()
        self.Contrasenia = self.Ctextarea.text().strip()

        if (self.bd.usuario_password_existen(self.Usuario, self.Contrasenia)):
            QMessageBox.information(self, "Inicio de sesión", f"Bienvenido, {self.Usuario}")
            self.Pventana = mainWindow(self.bd)
            self.Pventana.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")