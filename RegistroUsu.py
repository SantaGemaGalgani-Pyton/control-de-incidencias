import sys
from bbdd import BaseDeDatos
from VentanaPrincipal import VentanaPrincipal as mainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

"""Se crea la ventana de Registro de Usuarios"""
class VentanaPrincipal(QWidget):
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd

        """Titulo"""
        self.setWindowTitle("Registro")
        self.setGeometry(100, 100, 500, 350)

        """Creamos los textos"""
        self.Ulabel = QLabel("Usuario")
        self.Clabel = QLabel("Contraseña")

        """Creamos botones de Iniciar Sesion y Registrarse"""
        self.ISboton = QPushButton("Iniciar Sesión")
        self.ISboton.setFixedWidth(150)
        self.ISboton.setFixedHeight(35)

        self.Rboton = QPushButton("Registrarse")
        self.Rboton.setFixedWidth(150)
        self.Rboton.setFixedHeight(35)

        """Creamos las cajas de texto para recoger los datos del usuario"""
        self.Utextarea = QLineEdit()
        self.Ctextarea = QLineEdit()
        self.Ctextarea.setEchoMode(QLineEdit.Password)
        self.ISboton.clicked.connect(self.iniciarsesion)
        self.Rboton.clicked.connect(self.registrarse)

        """Hacemos los layouts para ordenar los diferentes elementos"""
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
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()
        if (self.bd.usuario_password_existen(self.Usuario, self.Contrasenia)):
            pass
        else:
            self.bd.anadir_usuario(self.Usuario, self.Contrasenia)
        """Registra el usuario en la base de datos"""

    def iniciarsesion(self):
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()
        if (self.bd.usuario_password_existen(self.Usuario, self.Contrasenia)):
            self.Pventana = mainWindow(self.bd)
            self.Pventana.show()
            self.close()
        else:
            pass
        """Comprueba que el usuario y la contraseña esten en la base de datos y abre la ventana principal si estan"""