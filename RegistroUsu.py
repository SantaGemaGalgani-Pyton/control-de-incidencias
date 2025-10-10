import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

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
        self.Utextarea.setFixedWidth(250)
        self.Utextarea.setFixedHeight(30)

        self.Ctextarea = QLineEdit()
        self.Ctextarea.setEchoMode(QLineEdit.Password)
        self.Ctextarea.setFixedWidth(250)
        self.Ctextarea.setFixedHeight(30)
    

        self.ISboton.clicked.connect(self.registrarse)
        self.Rboton.clicked.connect(self.iniciarsesion)

        layout = QVBoxLayout()
        layout.addWidget(self.Ulabel)
        layout.addWidget(self.Utextarea)
        layout.addWidget(self.Clabel)
        layout.addWidget(self.Ctextarea)
        layout.addWidget(self.ISboton)
        layout.addWidget(self.Rboton)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def registrarse(self):
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()

    def iniciarsesion(self):
        self.Usuario = self.Utextarea.text()
        self.Contrasenia = self.Ctextarea.text()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())