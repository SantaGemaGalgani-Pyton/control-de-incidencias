# ia/train_model.py
import os
import sqlite3
from pathlib import Path
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import joblib

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(exist_ok=True, parents=True)
MODEL_PATH = MODEL_DIR / "model.joblib"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.joblib"

DB_PATH = Path(__file__).resolve().parent.parent / "incidencias.db"

def fetch_data_from_db(db_path=DB_PATH) -> List[Tuple[str, str]]:
    """
    Devuelve lista de tuplas (texto, nivel_descripcion)
    """
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

def fallback_sample():
    # Pequeño conjunto de ejemplo si la BBDD está vacía
    return [
        ("La impresora no funciona, hace ruido y no sale papel", "Bajo"),
        ("Caída total del servidor, clientes no acceden a la web", "Alto"),
        ("Usuario no recuerda contraseña", "Bajo"),
        ("Pérdida de datos tras fallo actual, necesidad de recuperación urgente", "Alto"),
        ("Error intermitente en la aplicación, afecta a algunos usuarios", "Medio"),
        ("Pantalla azul al arrancar el equipo", "Medio"),
    ]

def prepare_dataset(rows):
    texts = [r[0] for r in rows]
    labels = [r[1] for r in rows]
    return texts, labels

def train_and_save(test_size=0.2, random_state=42):
    rows = fetch_data_from_db()
    if len(rows) < 10:
        # usamos fallback ampliando repetidos para que haya suficientes ejemplos
        rows = fallback_sample() * 5

    texts, labels = prepare_dataset(rows)

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=test_size, random_state=random_state, stratify=labels if len(set(labels))>1 else None
    )

    vect = TfidfVectorizer(ngram_range=(1,2), max_features=3000)
    clf = LogisticRegression(max_iter=1000)

    pipeline = make_pipeline(vect, clf)
    pipeline.fit(X_train, y_train)

    # guardar pipeline completo
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Modelo guardado en: {MODEL_PATH}")

    # también guardar vectorizer por si se quiere usar separadamente
    # (se obtiene desde pipeline.named_steps['tfidfvectorizer'] si hiciera falta)
    joblib.dump(vect, VECTORIZER_PATH)
    print(f"Vectorizer guardado en: {VECTORIZER_PATH}")

    # opcional: evaluamos rápidamente
    score = pipeline.score(X_test, y_test) if len(X_test)>0 else None
    if score is not None:
        print(f"Accuracy en test: {score:.3f}")
    else:
        print("No hay conjunto de test para evaluar (datos insuficientes).")

if __name__ == "__main__":
    train_and_save()
