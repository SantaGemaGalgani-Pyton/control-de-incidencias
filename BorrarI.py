import sys
import VentanaPrincipal
from PyQt5.QtWidgets import *

class BorrarI(QWidget):
    def __init__(self, bd):
        super().__init__()

        self.bd = bd

        self.setWindowTitle("Borrar Incidencia")
        self.setGeometry(100, 100, 640, 500)

        layout = QVBoxLayout()
        
        self.tabla = QTableWidget()
        self.tabla.setFixedWidth(615)
        self.tabla.setFixedHeight(300)
        self.tabla.setRowCount(1)
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(["ID", "Titulo", "Descripción", "Nivel", "Fecha", "Estado"])

        datos = [
            ["1", "t", "d", "n", "f", "e"]
        ]

        for fila in range(1):
            for col in range(6):
                self.tabla.setItem(fila, col, QTableWidgetItem(datos[fila][col]))

        self.BotonB = QPushButton("Borrar")
        self.BotonB.setFixedWidth(100)
        self.BotonB.setFixedHeight(35)
        # self.BotonB.clicked.connect(self.borrar)

        self.atrasBoton = QPushButton("Atrás")
        self.atrasBoton.setFixedWidth(100)
        self.atrasBoton.setFixedHeight(35)
        self.atrasBoton.clicked.connect(self.volver)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.atrasBoton)
        layout_botones.addSpacing(20)
        layout_botones.addWidget(self.BotonB)
        layout_botones.addStretch()

        layout.addWidget(self.tabla)
        layout.addLayout(layout_botones)

        self.setLayout(layout)

    # Consulta BBDD borrar
    def borrar(self):
        print("ALVARO BORRA BBDD")

    def volver(self):
        self.Pventana = VentanaPrincipal.VentanaPrincipal(self.bd)
        self.Pventana.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BorrarI()
    ventana.show()
    sys.exit(app.exec_())

