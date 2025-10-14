from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import graficos

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

        tipoIncidenciaYCuenta = [
            ("Bajo", 33, "#75DAFF"),
            ("Medio", 12, "#FFFF88"),
            ("Alto", 4, "#FF8A96")
        ]

        ax = graficos.GraficoNivelDeIncidencias(tipoIncidenciaYCuenta, "titulo")
        self.canvas.draw() 

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = CircularG()
    ventana.show()
    sys.exit(app.exec_())