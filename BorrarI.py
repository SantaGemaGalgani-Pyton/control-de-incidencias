import sys
import VentanaPrincipal
from bbdd import BaseDeDatos
from PyQt5.QtWidgets import *

class BorrarI(QWidget):
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd

        self.setWindowTitle("Borrar Incidencia")
        self.setGeometry(100, 100, 640, 500)

        layout = QVBoxLayout()
        
        self.tabla = QTableWidget()
        self.tabla.setFixedWidth(615)
        self.tabla.setFixedHeight(300)

        datos = bd.consultar_todas()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))
        self.tabla.setHorizontalHeaderLabels(["ID", "Descripción", "Nivel", "Fecha creación", "fecha resolución", "Estado"])

        self.poner_datos_en_tabla()

        self.BotonB = QPushButton("Borrar")
        self.BotonB.setFixedWidth(100)
        self.BotonB.setFixedHeight(35)
        self.BotonB.clicked.connect(self.borrar)

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

    def borrar(self):
        fila = self.tabla.currentRow()
        if fila == -1:
            QMessageBox.warning(self, "Error", "Por favor, selecciona una incidencia para borrar.")
            return

        id_incidencia = self.tabla.item(fila, 0).text()

        self.bd.borrar_incidencia(id_incidencia)

        self.poner_datos_en_tabla()

        QMessageBox.information(self, "Borrado", f"La incidencia con ID {id_incidencia} ha sido borrada correctamente.")


    def volver(self):
        self.Pventana = VentanaPrincipal.VentanaPrincipal(self.bd)
        self.Pventana.show()
        self.close()

    def poner_datos_en_tabla(self):
        datos = self.bd.consultar_todas_id()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))
        
        for fila, datos in enumerate(datos):
            for col, valor in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = BorrarI()
    ventana.show()
    sys.exit(app.exec_())