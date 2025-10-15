import sys
from bbdd import BaseDeDatos
import RegistroIncidencias, BorrarI, graficos
from PyQt5.QtWidgets import *

class VentanaPrincipal(QMainWindow):
    def __init__(self, bd: BaseDeDatos):
        super().__init__()

        self.bd = bd

        self.setWindowTitle("Incidencias")
        self.setGeometry(100, 100, 700, 400)

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

        tiempo_resolucion_accion = QAction("Tiempo de Resolución", self)
        tiempo_resolucion_accion.triggered.connect(self.abrirGTR)

        grafico_menu.addAction(gravedad_accion)
        grafico_menu.addAction(estado_accion)
        grafico_menu.addAction(tiempo_resolucion_accion)

        exportar_menu = menubar.addMenu("Exportar")

        pdf_menu = exportar_menu.addMenu("PDF")

        PDFGestado_accion = QAction("Grafico Gravedad", self)
        PDFGestado_accion.triggered.connect(self.exportarPDFge)

        PDFGnivel_accion = QAction("Grafico Nivel", self)
        PDFGnivel_accion.triggered.connect(self.exportarPDFgn)

        PDFGtiempo_accion = QAction("Grafico Tiempo Resolucion", self)
        PDFGtiempo_accion.triggered.connect(self.exportarPDFgt)

        csv_menu = exportar_menu.addMenu("CSV")

        CSVGestado_accion = QAction("Grafico Gravedad", self)
        CSVGestado_accion.triggered.connect(self.exportarCSVge)

        CSVGnivel_accion = QAction("Grafico Nivel", self)
        CSVGnivel_accion.triggered.connect(self.exportarCSVgn)

        CSVGtiempo_accion = QAction("Grafico Tiempo Resolucion", self)
        CSVGtiempo_accion.triggered.connect(self.exportarCSVgt)

        exportar_menu.addMenu(pdf_menu)

        pdf_menu.addAction(PDFGestado_accion)
        pdf_menu.addAction(PDFGnivel_accion)
        pdf_menu.addAction(PDFGtiempo_accion)

        exportar_menu.addMenu(csv_menu)

        csv_menu.addAction(CSVGestado_accion)
        csv_menu.addAction(CSVGnivel_accion)
        csv_menu.addAction(CSVGtiempo_accion)

        central_widget = QWidget()
        layout = QVBoxLayout()

        datos = bd.consultar_todas()

        self.tabla = QTableWidget()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))
        self.tabla.setHorizontalHeaderLabels(["Descripción", "Nivel", "Fecha creación", "Fecha resolución", "Estado"])
        self.tabla.setFixedHeight(300)

        for fila, datos in enumerate(datos):
            for col, valor in enumerate(datos):
                self.tabla.setItem(fila, col, QTableWidgetItem(valor))

        layout.addWidget(self.tabla)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def abrirRI(self):
        self.registro = RegistroIncidencias.RI(self.bd)
        self.registro.show()
        self.close()
    
    def abrirBI(self):
        self.registro = BorrarI.BorrarI(self.bd)
        self.registro.show()
        self.close()
    
    def abrirGG(self):
        self.registro = graficos.GraficoNivelDeIncidencias(self.bd.incidencias_gravedad())

    def abrirGE(self):
        self.registro = graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado())

    def abrirGTR(self):
        self.registro = graficos.GraficoEstadoDeIncidencias(self.bd.incidencias_estado())

    def abrirGTR(self):
        #self.registro = graficos.()
        self.registro.show()
        self.close()

    def exportarPDFge(self):
        graficos.ExportarAPDF(graficos.GraficoEstadoDeIncidencias)

    def exportarCSVge(self):
        graficos.ExportarACSV(graficos.GraficoEstadoDeIncidencias)

    def exportarPDFgn(self):
        graficos.ExportarAPDF(graficos.GraficoNivelDeIncidencias)

    def exportarCSVgn(self):
        graficos.ExportarACSV(graficos.GraficoNivelDeIncidencias)

    def exportarPDFgt(self):
        graficos.ExportarAPDF(graficos.GraficoTiempoDeIncidencias)

    def exportarCSVgt(self):
        graficos.ExportarACSV(graficos.GraficoTiempoDeIncidencias)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
