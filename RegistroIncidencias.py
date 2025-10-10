import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QLineEdit
from PyQt5.QtCore import Qt

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro de Incidencias")
        self.setGeometry(100, 100, 500, 350)

        self.Nlabel = QLabel("Nombre Incidencia")
        self.Elabel = QLabel("Estado")
        self.Plabel = QLabel("Prioridad")
        self.Flabel = QLabel("Fecha")

        self.Gboton = QPushButton("Guardar Incidencia")
        self.Gboton.setFixedWidth(150)
        self.Gboton.setFixedHeight(35)

        self.Bboton = QPushButton("Borrar")
        self.Bboton.setFixedWidth(150)
        self.Bboton.setFixedHeight(35)

        self.Ntextarea = QLineEdit()
        self.Ntextarea.setFixedWidth(250)
        self.Ntextarea.setFixedHeight(30)

        self.Etextarea = QLineEdit()
        self.Etextarea.setFixedWidth(250)
        self.Etextarea.setFixedHeight(30)

        self.Ptextarea = QLineEdit()
        self.Ptextarea.setFixedWidth(250)
        self.Ptextarea.setFixedHeight(30)
    
        self.Ftextarea = QLineEdit()
        self.Ftextarea.setFixedWidth(250)
        self.Ftextarea.setFixedHeight(30)

        self.Gboton.clicked.connect(self.guardar)
        self.Bboton.clicked.connect(self.borrar)

        layout = QVBoxLayout()
        layout.addWidget(self.Nlabel)
        layout.addWidget(self.Ntextarea)
        layout.addWidget(self.Elabel)
        layout.addWidget(self.Etextarea)
        layout.addWidget(self.Plabel)
        layout.addWidget(self.Ptextarea)
        layout.addWidget(self.Flabel)
        layout.addWidget(self.Ftextarea)

        layout.addWidget(self.Gboton)
        layout.addWidget(self.Bboton)
        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

    def guardar(self):
        self.Nombre = self.Ntextarea.text()
        self.Estado = self.Etextarea.text()
        self.Prioridad = self.Ptextarea.text()
        self.Fecha = self.Ftextarea.text()

    def borrar(self):
        self.Ntextarea.clear()
        self.Etextarea.clear()
        self.Ptextarea.clear()
        self.Ftextarea.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())