"""
Entrenamiento de modelos para:
- prioridad (Nivel)  -> clasificación (puede ser ordinal pero tratamos como clasificación)
- categoria (si existe) -> clasificación multi-clase

Uso:
 python ia/train_model.py --db path/to/bbddincidencias.db
 or
 python ia/train_model.py --csv path/to/labeled.csv

El script guarda:
 - ia/tfidf_vectorizer.joblib
 - ia/model_priority.joblib
 - ia/model_category.joblib (si hay etiquetas de categoria)
"""

import argparse
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Ruta de salida
OUT_DIR = "ia"
os.makedirs(OUT_DIR, exist_ok=True)

def load_from_sqlite(db_path):
    import sqlite3
    conn = sqlite3.connect(db_path)
    # Intentamos seleccionar las columnas que puedan existir
    query = """
    SELECT ID, Titulo, Descripción_Detallada AS descripcion, Nivel AS prioridad, 
           COALESCE(Categoria, Tipo, '') AS categoria
    FROM incidencia
    """
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        # Fallback con nombres en ingles o distintos
        query2 = "SELECT ID, Titulo, Descripcion_Detallada AS descripcion, Nivel AS prioridad FROM incidencia"
        df = pd.read_sql_query(query2, conn)
        # añade columna categoria vacía
        if 'categoria' not in df.columns:
            df['categoria'] = ''
    conn.close()
    return df

def load_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    # Normalizar nombres de columnas
    cols = {c.lower(): c for c in df.columns}
    # Busca columnas típicas
    mapping = {}
    for key in ['descripcion','descripcion_detallada','descripcion_detalhada','description','text']:
        if key in cols:
            mapping[cols[key]] = 'descripcion'
            break
    for key in ['prioridad','nivel','level','priority']:
        if key in cols:
            mapping[cols[key]] = 'prioridad'
            break
    for key in ['categoria','category','type','tipo']:
        if key in cols:
            mapping[cols[key]] = 'categoria'
            break
    df = df.rename(columns=mapping)
    if 'categoria' not in df.columns:
        df['categoria'] = ''
    return df

def prepare_data(df):
    # Concatenate titulo y descripcion
    if 'Titulo' in df.columns:
        df['texto'] = df['Titulo'].fillna('') + '. ' + df['descripcion'].fillna('')
    else:
        df['texto'] = df['descripcion'].fillna('')

    # Drop empty texts
    df = df[df['texto'].str.strip() != '']
    # Prioridad: si no existe, intentar derivar de 'prioridad' o dejar NaN
    if 'prioridad' not in df.columns and 'prioridad' not in df.columns:
        df['prioridad'] = df.get('Nivel', np.nan)
    df['prioridad'] = df['prioridad'].replace('', np.nan)
    return df

def train_priority(X_train, y_train):
    # Clasificador simple: LogisticRegression (multiclase), con TF-IDF pipeline
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=15000, ngram_range=(1,2), stop_words='spanish')),
        ('clf', LogisticRegression(max_iter=200))
    ])
    pipe.fit(X_train, y_train)
    return pipe

def train_category(X_train, y_train):
    # MultinomialNB suele ir bien para texto multi-clase
    pipe = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=15000, ngram_range=(1,2), stop_words='spanish')),
        ('clf', MultinomialNB())
    ])
    pipe.fit(X_train, y_train)
    return pipe

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', help='ruta a la base de datos sqlite')
    parser.add_argument('--csv', help='ruta a CSV con columnas descripcion, prioridad, categoria')
    parser.add_argument('--test-size', type=float, default=0.2)
    parser.add_argument('--force-synthetic', action='store_true', help='crear dataset sintético de prueba si no hay etiquetas')
    args = parser.parse_args()

    if args.db:
        df = load_from_sqlite(args.db)
    elif args.csv:
        df = load_from_csv(args.csv)
    else:
        raise SystemExit("Pasa --db or --csv con datos.")

    df = prepare_data(df)

    # PRIORIDAD
    if df['prioridad'].notna().sum() < 10:
        if args.force_synthetic:
            print("Pocas etiquetas de prioridad; generando etiquetas sintéticas (solo para demo).")
            # asignar prioridades aleatorias 1..3
            np.random.seed(42)
            df['prioridad'] = np.random.choice([1,2,3], size=len(df))
        else:
            print("Pocas etiquetas de prioridad. Usa --force-synthetic para demo o provee más datos.")
            # seguimos pero con advertencia
            df['prioridad'] = df['prioridad'].fillna(1)

    # CATEGORIA
    has_category = False
    if 'categoria' in df.columns and df['categoria'].astype(str).str.strip().sum() > 0:
        df['categoria'] = df['categoria'].fillna('').astype(str)
        if df['categoria'].str.strip().nunique() > 1:
            has_category = True
    else:
        if args.force_synthetic:
            print("Generando categorías sintéticas para demo.")
            # categorías sintéticas
            choices = ['red', 'hardware', 'software', 'usuario', 'red']
            np.random.seed(0)
            df['categoria'] = np.random.choice(choices, size=len(df))
            has_category = True
        else:
            print("No se detectaron etiquetas de categoria. Para entrenar categoria pasa --force-synthetic o un CSV con columna 'categoria'.")

    # Entrenamiento prioridad
    X = df['texto'].values
    y_prio = df['prioridad'].astype(str).values  # tratar como string para clasificación
    X_train, X_test, y_train, y_test = train_test_split(X, y_prio, test_size=args.test_size, random_state=42, stratify=y_prio)

    print("Entrenando modelo de prioridad...")
    model_prio = train_priority(X_train, y_train)
    preds = model_prio.predict(X_test)
    print("Reporte prioridad:")
    print(classification_report(y_test, preds))
    acc = accuracy_score(y_test, preds)
    print(f"Exactitud prioridad: {acc:.3f}")

    # Guardar
    joblib.dump(model_prio, os.path.join(OUT_DIR, "model_priority.joblib"))
    print("Modelo de prioridad guardado en ia/model_priority.joblib")

    # Entrenamiento categoria si procede
    if has_category:
        y_cat = df['categoria'].values
        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_cat, test_size=args.test_size, random_state=42, stratify=y_cat)
        print("Entrenando modelo de categoria...")
        model_cat = train_category(X_train_c, y_train_c)
        preds_cat = model_cat.predict(X_test_c)
        print("Reporte categoria:")
        print(classification_report(y_test_c, preds_cat))
        joblib.dump(model_cat, os.path.join(OUT_DIR, "model_category.joblib"))
        print("Modelo de categoria guardado en ia/model_category.joblib")
    else:
        print("No se entrenó modelo de categoría (falta etiqueta).")

if __name__ == "__main__":
    main()
