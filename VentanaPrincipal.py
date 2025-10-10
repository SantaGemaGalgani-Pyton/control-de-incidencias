import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ejemplo Menubar")
        self.setGeometry(100, 100, 400, 300)

        # Crear la barra de menú
        menubar = self.menuBar()

        # Crear menú "Archivo"
        archivo_menu = menubar.addMenu("Archivo")

        # Crear acciones
        nuevo_accion = QAction("Nuevo", self)
        abrir_accion = QAction("Abrir", self)
        salir_accion = QAction("Salir", self)
        salir_accion.triggered.connect(self.close)  # Cierra la ventana

        # Añadir acciones al menú
        archivo_menu.addAction(nuevo_accion)
        archivo_menu.addAction(abrir_accion)
        archivo_menu.addSeparator()  # Línea separadora
        archivo_menu.addAction(salir_accion)

        # Otro menú
        ayuda_menu = menubar.addMenu("Ayuda")
        acerca_accion = QAction("Acerca de", self)
        ayuda_menu.addAction(acerca_accion)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())