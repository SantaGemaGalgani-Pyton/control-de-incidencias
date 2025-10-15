from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class CircularG(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico Circular")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # Crear figura de Matplotlib
        self.figura = Figure()
        self.canvas = FigureCanvas(self.figura)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # Datos del gráfico
        tipoIncidenciaYCuenta = [
            ("Bajo", 33),
            ("Medio", 12),
            ("Alto", 4)
        ]

        # Llamar a la función para dibujar el gráfico circular
        self.dibujar_grafico(tipoIncidenciaYCuenta, "Incidencias por Nivel")

    def dibujar_grafico(self, datos, titulo):
        # Extraer etiquetas y valores
        etiquetas = [item[0] for item in datos]
        valores = [item[1] for item in datos]

        # Crear un eje en la figura
        ax = self.figura.add_subplot(111)
        ax.clear()  # Limpiar por si se redibuja

        # Dibujar gráfico circular
        ax.pie(valores, labels=etiquetas, autopct='%1.1f%%')
        ax.set_title(titulo)

        # Actualizar canvas
        self.canvas.draw()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = CircularG()
    ventana.show()
    sys.exit(app.exec_())
