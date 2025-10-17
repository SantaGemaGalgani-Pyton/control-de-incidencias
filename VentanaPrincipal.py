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

        estado_accion = QAction("Nivel", self)
        estado_accion.triggered.connect(self.abrirGE)

        grafico_menu.addAction(gravedad_accion)
        grafico_menu.addAction(estado_accion)

        exportar_menu = menubar.addMenu("Exportar")

        pdf_menu = exportar_menu.addMenu("PDF")

        PDFGestado_accion = QAction("Grafico Gravedad", self)
        PDFGestado_accion.triggered.connect(self.exportarPDFge)

        PDFGnivel_accion = QAction("Grafico Nivel", self)
        PDFGnivel_accion.triggered.connect(self.exportarPDFgn)

        csv_menu = exportar_menu.addMenu("CSV")

        CSVGestado_accion = QAction("Grafico Gravedad", self)
        CSVGestado_accion.triggered.connect(self.exportarCSVge)

        CSVGnivel_accion = QAction("Grafico Nivel", self)
        CSVGnivel_accion.triggered.connect(self.exportarCSVgn)

        exportar_menu.addMenu(pdf_menu)

        pdf_menu.addAction(PDFGestado_accion)
        pdf_menu.addAction(PDFGnivel_accion)

        exportar_menu.addMenu(csv_menu)

        csv_menu.addAction(CSVGestado_accion)
        csv_menu.addAction(CSVGnivel_accion)

        filtros_menu = menubar.addMenu("Filtros")

        filtrar_estado_accion = QAction("Filtrar por Estado", self)
        filtrar_estado_accion.triggered.connect(lambda: self.filtrar_tabla("Estado"))

        filtrar_nivel_accion = QAction("Filtrar por Nivel", self)
        filtrar_nivel_accion.triggered.connect(lambda: self.filtrar_tabla("Nivel"))

        filtrar_fecha_accion = QAction("Filtrar por Fecha", self)
        filtrar_fecha_accion.triggered.connect(lambda: self.filtrar_tabla("Fecha creación"))

        mostrar_todos_accion = QAction("Mostrar todos", self)
        mostrar_todos_accion.triggered.connect(lambda: self.filtrar_tabla("Todos"))

        filtros_menu.addAction(filtrar_estado_accion)
        filtros_menu.addAction(filtrar_nivel_accion)
        filtros_menu.addAction(filtrar_fecha_accion)
        filtros_menu.addSeparator()
        filtros_menu.addAction(mostrar_todos_accion)

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

        if fila == -1:
            QMessageBox.warning(self, "Error", "Selecciona una fila primero.")
            return

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
        self.registro = graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado())

    def exportarPDFge(self):
        graficos.ExportarAPDF(graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado(), False))

    def exportarCSVge(self):
        graficos.ExportarACSV(graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado(), False))

    def exportarPDFgn(self):
        graficos.ExportarAPDF(graficos.GraficoNivelDeIncidencias(self.bd.incidencias_gravedad(), False))

    def exportarCSVgn(self):
        graficos.ExportarACSV(graficos.GraficoNivelDeIncidencias(self.bd.incidencias_gravedad(), False))

    def filtrar_tabla(self, criterio):
        if criterio == "Todos":
            for fila in range(self.tabla.rowCount()):
                self.tabla.setRowHidden(fila, False)
            return
    
        valor, ok = QInputDialog.getText(self, "Filtrar", f"Ingrese {criterio}:")
        if not ok or not valor:
            return

        if criterio == "Estado":
            col = 4
        elif criterio == "Nivel":
            col = 1
        elif criterio == "Fecha creación":
            col = 2
        else:
            return

        for fila in range(self.tabla.rowCount()):
            item = self.tabla.item(fila, col)
            if item and item.text() == valor:
                self.tabla.setRowHidden(fila, False)
            else:
                self.tabla.setRowHidden(fila, True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
