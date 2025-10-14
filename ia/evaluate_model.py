"""
Evaluación rápida de modelos guardados.
Uso:
 python ia/evaluate_model.py --db path/to/bbddincidencias.db
"""
import argparse
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score

def load_data_from_db(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    query = "SELECT Titulo, Descripción_Detallada AS descripcion, Nivel AS prioridad, COALESCE(Categoria, Tipo, '') AS categoria FROM incidencia"
    try:
        df = pd.read_sql_query(query, conn)
    except Exception:
        query2 = "SELECT Titulo, Descripcion_Detallada AS descripcion, Nivel AS prioridad FROM incidencia"
        df = pd.read_sql_query(query2, conn)
        df['categoria'] = ''
    conn.close()
    df['texto'] = df['Titulo'].fillna('') + '. ' + df['descripcion'].fillna('')
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True)
    args = parser.parse_args()

    df = load_data_from_db(args.db)
    texts = df['texto'].astype(str).values

    # cargar modelos si existen
    try:
        model_prio = joblib.load("ia/model_priority.joblib")
    except:
        print("No se encontró ia/model_priority.joblib")
        return
    y_true_prio = df['prioridad'].astype(str).fillna('0').values
    y_pred_prio = model_prio.predict(texts)
    print("Prioridad - accuracy:", accuracy_score(y_true_prio, y_pred_prio))
    print(classification_report(y_true_prio, y_pred_prio))

    try:
        model_cat = joblib.load("ia/model_category.joblib")
        y_true_cat = df['categoria'].astype(str).fillna('').values
        y_pred_cat = model_cat.predict(texts)
        print("Categoria - accuracy:", accuracy_score(y_true_cat, y_pred_cat))
        print(classification_report(y_true_cat, y_pred_cat))
    except:
        print("No se encontró modelo de categoria (ia/model_category.joblib).")

if __name__ == "__main__":
    main()
