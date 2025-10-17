# ia/pyqt_integration_snippet.py
from pathlib import Path
import joblib
from typing import Optional

MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.joblib"

def load_pipeline():
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)

_pipeline = None

def predict_level_from_text(text: str) -> Optional[str]:
    """
    Devuelve la predicción del nivel (ej. 'Bajo', 'Medio', 'Alto')
    o None si no hay modelo.
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = load_pipeline()
    if _pipeline is None:
        return None
    return _pipeline.predict([text])[0]

# Ejemplo de uso dentro de PyQt (pseudocódigo / guía):
pyqt_integration_example = """
# En tu formulario de registro (ejemplo simplificado):
from PyQt5.QtWidgets import QPushButton, QLineEdit, QComboBox
from ia.pyqt_integration_snippet import predict_level_from_text

# supongamos que tienes:
# self.descripcion_textedit -> QLineEdit o QTextEdit
# self.nivel_combobox -> QComboBox con opciones ('Bajo', 'Medio', 'Alto')
# self.auto_predict_btn -> QPushButton

def on_auto_predict_clicked(self):
    texto = self.descripcion_textedit.toPlainText() if hasattr(self.descripcion_textedit, 'toPlainText') else self.descripcion_textedit.text()
    pred = predict_level_from_text(texto)
    if pred:
        # intentar seleccionar el índice correspondiente en combobox
        idx = self.nivel_combobox.findText(pred)
        if idx != -1:
            self.nivel_combobox.setCurrentIndex(idx)
        else:
            # si no existe la opción, añadirla y seleccionarla
            self.nivel_combobox.addItem(pred)
            self.nivel_combobox.setCurrentText(pred)
    else:
        QMessageBox.information(self, "Modelo IA", "Modelo no disponible. Entrena primero (ia/train_model.py).")
"""
