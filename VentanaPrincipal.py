import sys
from bbdd import BaseDeDatos
import RegistroIncidencias, BorrarI, graficos
from PyQt5.QtWidgets import *

class VentanaPrincipal(QMainWindow):
    """Se crea la ventana principal"""
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd
        
        """Titulo"""
        self.setWindowTitle("Incidencias")
        self.setGeometry(100, 100, 700, 400)

        """Se crea el menu con sus distintos botones"""
        menubar = self.menuBar()
        incidencias_menu = menubar.addMenu("Incidencias")

        nuevo_accion = QAction("Nuevo", self)
        nuevo_accion.triggered.connect(self.abrirRI)

        borrar_accion = QAction("Borrar", self)
        borrar_accion.triggered.connect(self.abrirBI)

        salir_accion = QAction("Salir", self)
        salir_accion.triggered.connect(self.close)

        incidencias_menu.addAction(nuevo_accion)
        incidencias_menu.addAction(borrar_accion)
        incidencias_menu.addAction(salir_accion)

        grafico_menu = menubar.addMenu("Graficos")

        gravedad_accion = QAction("Gravedad", self)
        gravedad_accion.triggered.connect(self.abrirGG)

        estado_accion = QAction("Estado", self)
        estado_accion.triggered.connect(self.abrirGE)

        tiempo_resolucion_accion = QAction("Tiempo de Resolución", self)
        tiempo_resolucion_accion.triggered.connect(self.abrirGTR)

        grafico_menu.addAction(gravedad_accion)
        grafico_menu.addAction(estado_accion)
        grafico_menu.addAction(tiempo_resolucion_accion)

        central_widget = QWidget()
        layout = QVBoxLayout()

        datos = bd.consultar_todas()
        
        """Se crea la tabla y se añade a la ventana"""
        self.tabla = QTableWidget()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Nivel", "Fecha creación", "Fecha resolución", "Estado"])
        self.tabla.setFixedHeight(300)

        for fila, datos in enumerate(datos):
            for col, valor in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(valor))
        
        self.BotonCE = QPushButton("Cambiar Estado")
        self.BotonCE.setFixedWidth(100)
        self.BotonCE.setFixedHeight(35)
        self.BotonCE.clicked.connect(self.cambiarEstado)

        layout.addWidget(self.tabla)
        layout.addWidget(self.BotonCE)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def cambiarEstado(self):
        fila = self.tabla.currentRow()
        self.bd.actualizar_estado(self.tabla.item(fila, 0).text())
        self.poner_datos_en_tabla()

    def poner_datos_en_tabla(self):
        datos = self.bd.consultar_todas_id()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))
        
        for fila, datos in enumerate(datos):
            for col, valor in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(str(valor)))

    def abrirRI(self):
        self.registro = RegistroIncidencias.RI(self.bd)
        self.registro.show()
        self.close()
    """Abre el Registro de incidencias"""

    def abrirBI(self):
        self.registro = BorrarI.BorrarI(self.bd)
        self.registro.show()
        self.close()
    """Abre el Borrar incidencias"""

    def abrirGG(self):
        self.registro = graficos.GraficoNivelDeIncidencias(self.bd.incidencias_gravedad())
    """Abre el Gráfico de gravedad"""

    def abrirGE(self):
        self.registro = graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado())
    """Abre el grafico de estado"""

    def abrirGTR(self):
        #self.registro = graficos.()
        self.registro.show()
        self.close()
    """Abre el grafico de tiempo de registro"""

