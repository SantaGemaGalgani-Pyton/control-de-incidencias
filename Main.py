import sys
from RegistroUsu import VentanaPrincipal
import bbdd;
from PyQt5.QtWidgets import *

def Main():
    app = QApplication(sys.argv)
    bd = bbdd.BaseDeDatos()
    ventana = VentanaPrincipal(bd)
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    Main()