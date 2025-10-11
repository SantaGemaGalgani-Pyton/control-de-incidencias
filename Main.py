import sys
import RegistroUsu
from PyQt5.QtWidgets import *

def Main():
    app = QApplication(sys.argv)
    ventana = RegistroUsu.VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Main()