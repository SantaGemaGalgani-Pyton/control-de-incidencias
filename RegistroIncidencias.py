import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QCalendarWidget, QHBoxLayout
from PyQt5.QtCore import Qt, QDate

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro de Incidencias")
        self.setGeometry(100, 100, 500, 350)

        self.Nlabel = QLabel("Nombre Incidencia")
        self.Plabel = QLabel("Prioridad")
        self.Flabel = QLabel("Fecha")

        self.Gboton = QPushButton("Guardar Incidencia")
        self.Gboton.setFixedWidth(150)
        self.Gboton.setFixedHeight(35)

        self.Bboton = QPushButton("Borrar")
        self.Bboton.setFixedWidth(150)
        self.Bboton.setFixedHeight(35)

        self.Ntextarea = QLineEdit()

        self.Ptextarea = QComboBox()
        opciones = ["Opción 1", "Opción 2", "Opción 3"]
        self.Ptextarea.addItems(opciones)

        self.fecha = QLineEdit()
        self.fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        self.fecha.setReadOnly(True)
        self.fecha.mousePressEvent = self.mostrarCalendario

        self.Fcalendar = QCalendarWidget()
        self.Fcalendar.setWindowFlags(self.Fcalendar.windowFlags() | Qt.Popup)
        self.Fcalendar.clicked.connect(self.seleccionarFecha)

        self.Gboton.clicked.connect(self.guardar)
        self.Bboton.clicked.connect(self.borrar)

        self.atrasBoton = QPushButton("Atrás")
        self.atrasBoton.setFixedWidth(100)
        self.atrasBoton.setFixedHeight(35)
        self.atrasBoton.clicked.connect(self.volver)

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
        self.Nombre = self.Ntextarea.text()
        self.Prioridad = self.Ptextarea.currentText()
        self.Fecha = self.fecha.text()

    def borrar(self):
        self.Ntextarea.clear()
        self.Ptextarea.setCurrentIndex(0)
        self.fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))

    def mostrarCalendario(self, event):
        self.Fcalendar.move(self.fecha.mapToGlobal(self.fecha.rect().bottomLeft()))
        self.Fcalendar.show()

    def seleccionarFecha(self, date):
        self.fecha.setText(date.toString("dd/MM/yyyy"))
        self.Fcalendar.hide()
    
    def volver(self):

        ventana.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
