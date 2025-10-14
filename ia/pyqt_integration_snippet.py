"""
Ejemplo de integración en PyQt (función que se llama cuando se cambia la descripción
o se quiere predecir al crear/incidencia seleccionar).
Requiere `requests`.
"""
import requests
from PyQt5.QtWidgets import QMessageBox

API_URL = "http://127.0.0.1:8001/predict"

def predecir_incidencia_y_mostrar(texto, parent_widget=None):
    """
    texto: str con título + descripción.
    parent_widget: QWidget (opcional) para mostrar mensajes.
    """
    if not texto or texto.strip() == "":
        return None
    try:
        resp = requests.post(API_URL, json={"texto": texto}, timeout=3.0)
        if resp.status_code == 200:
            data = resp.json()
            prioridad = data.get('prioridad')
            categoria = data.get('categoria')
            # ejemplo: actualizar campos de la GUI
            # self.lineEdit_prioridad.setText(str(prioridad))
            # self.combo_categoria.setCurrentText(categoria)
            # Muestro popup breve si hay parent_widget
            if parent_widget:
                QMessageBox.information(parent_widget, "Predicción IA", f"Prioridad: {prioridad}\nCategoría: {categoria}")
            return data
        else:
            if parent_widget:
                QMessageBox.warning(parent_widget, "Error IA", f"Error en API: {resp.status_code}")
            return None
    except Exception as e:
        if parent_widget:
            QMessageBox.warning(parent_widget, "Error IA", f"No se pudo conectar al servicio IA:\n{e}")
        return None

# Ejemplo de uso:
# texto = titulo + ". " + descripcion
# data = predecir_incidencia_y_mostrar(texto, parent_widget=self)
