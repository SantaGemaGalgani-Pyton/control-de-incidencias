import sys
import VentanaPrincipal
from bbdd import BaseDeDatos
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class RI(QWidget):
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd

        """Titulo"""
        self.setWindowTitle("Registro de Incidencias")
        self.setGeometry(100, 100, 500, 350)

        """Creamos los textos"""
        self.Nlabel = QLabel("Nombre Incidencia")
        self.Plabel = QLabel("Prioridad")
        self.Flabel = QLabel("Fecha")

        """Creamos los botones para guardar o borrar incidencias"""
        self.Gboton = QPushButton("Guardar Incidencia")
        self.Gboton.setFixedWidth(150)
        self.Gboton.setFixedHeight(35)

        self.Bboton = QPushButton("Borrar")
        self.Bboton.setFixedWidth(150)
        self.Bboton.setFixedHeight(35)

        """Creamos las cajas de texto para recoger los datos de la incidencia"""
        self.Ntextarea = QLineEdit()
        self.Ptextarea = QComboBox()
        op = []
        for fila in self.bd.nombres_niveles():
            op.append(fila[0])
        opciones = op
        self.Ptextarea.addItems(opciones)

        self.fecha = QLineEdit()
        self.fecha.setText(QDate.currentDate().toString("dd-MM-yyyy"))
        self.fecha.setReadOnly(True)
        self.fecha.mousePressEvent = self.mostrarCalendario

        self.Fcalendar = QCalendarWidget()
        self.Fcalendar.setWindowFlags(self.Fcalendar.windowFlags() | Qt.Popup)
        self.Fcalendar.clicked.connect(self.seleccionarFecha)

        """Indicamos que hace cada boton"""
        self.Gboton.clicked.connect(self.guardar)
        self.Bboton.clicked.connect(self.borrar)

        self.atrasBoton = QPushButton("Atrás")
        self.atrasBoton.setFixedWidth(100)
        self.atrasBoton.setFixedHeight(35)
        self.atrasBoton.clicked.connect(self.volver)

        """Hacemos los layouts para ordenar los diferentes elementos"""
        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(self.Gboton)
        layout_botones.addSpacing(20)
        layout_botones.addWidget(self.Bboton)
        layout_botones.addStretch() 

        layout = QVBoxLayout()
        layout.addWidget(self.Nlabel) 
        layout.addWidget(self.Ntextarea)
        layout.addWidget(self.Plabel)
        layout.addWidget(self.Ptextarea)
        layout.addWidget(self.Flabel)
        layout.addWidget(self.fecha)

        layout.addLayout(layout_botones) 

        layout.setContentsMargins(50, 30, 50, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        layout.addWidget(self.atrasBoton, alignment=Qt.AlignCenter)

    def guardar(self):
        self.Nombre = self.Ntextarea.text().strip()
        self.Prioridad = self.Ptextarea.currentIndex() + 1
        self.Fecha = self.fecha.text()

        if not self.Nombre:
            QMessageBox.warning(self, "Error", "El nombre de la incidencia no puede estar vacío.")
            return

        self.bd.crear_incidencia(self.Nombre, self.Prioridad, self.Fecha)
        """Guarda los elementos en la base de datos"""

        QMessageBox.information(self, "Incidencia creada", "La incidencia ha sido guardada correctamente.")

        self.Ntextarea.clear()
        self.Ptextarea.setCurrentIndex(0)
        self.fecha.setText(QDate.currentDate().toString("dd-MM-yyyy"))


    def borrar(self):
        self.Ntextarea.clear()
        self.Ptextarea.setCurrentIndex(0)
        self.fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        """Borra todo lo cambiado dentro de la ventana"""

    def mostrarCalendario(self, event):
        self.Fcalendar.move(self.fecha.mapToGlobal(self.fecha.rect().bottomLeft()))
        self.Fcalendar.show()
        """Muestra el calendario"""

    def seleccionarFecha(self, date):
        self.fecha.setText(date.toString("dd/MM/yyyy"))
        self.Fcalendar.hide()
        """Selecciona la fecha del calendario"""
    
    def volver(self):
        self.Pventana = VentanaPrincipal.VentanaPrincipal(self.bd)
        self.Pventana.show()
        self.close()
        """Vuelve a la ventana principal"""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = RI()
    ventana.show()
    sys.exit(app.exec_())