# ia/evaluate_model.py
import os
import sqlite3
from pathlib import Path
from typing import List, Tuple

import joblib
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

DB_PATH = Path(__file__).resolve().parent.parent / "incidencias.db"
MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.joblib"

def fetch_data_from_db(db_path=DB_PATH):
    if not db_path.exists():
        return []
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("""
        SELECT i.Descripcion_Detallada, n.Descripcion_Detallada
        FROM Incidencia i
        LEFT JOIN Niveles n ON i.Nivel = n.Numero
        WHERE i.Descripcion_Detallada IS NOT NULL AND n.Descripcion_Detallada IS NOT NULL
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def evaluate():
    rows = fetch_data_from_db()
    if not rows:
        print("No hay datos en la BBDD para evaluar.")
        return

    texts = [r[0] for r in rows]
    labels = [r[1] for r in rows]

    if not MODEL_PATH.exists():
        print("No se encuentra el modelo. Entrena primero (ejecuta ia/train_model.py).")
        return

    pipeline = joblib.load(MODEL_PATH)
    preds = pipeline.predict(texts)
    acc = accuracy_score(labels, preds)
    print(f"Accuracy: {acc:.3f}\n")
    print("Classification report:")
    print(classification_report(labels, preds))
    print("Confusion matrix:")
    print(confusion_matrix(labels, preds))

if __name__ == "__main__":
    evaluate()
