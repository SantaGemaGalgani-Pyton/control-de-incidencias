"""
API ligera para predicciones en tiempo real.

Endpoints:
 - POST /predict
   Body JSON: {"texto": "descripcion de la incidencia"}
   Response: {"prioridad": "1", "categoria": "hardware", "probs": {...}}

Ejecutar:
 uvicorn ia.predict_api:app --reload --port 8001
"""
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

app = FastAPI(title="API de Predicción - Control Incidencias")

MODEL_PRIO = os.path.join("ia","model_priority.joblib")
MODEL_CAT = os.path.join("ia","model_category.joblib")

# Cargar modelos (si existen)
model_prio = None
model_cat = None
if os.path.exists(MODEL_PRIO):
    model_prio = joblib.load(MODEL_PRIO)
else:
    print("Warning: modelo de prioridad no encontrado en", MODEL_PRIO)
if os.path.exists(MODEL_CAT):
    model_cat = joblib.load(MODEL_CAT)
else:
    print("Advertencia: modelo de categoría no encontrado:", MODEL_CAT)

class IncidenciaIn(BaseModel):
    texto: str

@app.post("/predict")
def predict(item: IncidenciaIn):
    texto = item.texto
    result = {}
    if model_prio:
        prio_pred = model_prio.predict([texto])[0]
        # intentar extraer probabilidades si el modelo tiene predict_proba
        probs_prio = None
        try:
            probs_prio = model_prio.predict_proba([texto])[0].tolist()
            classes_prio = model_prio.classes_.tolist()
            probs_prio = dict(zip(classes_prio, probs_prio))
        except Exception:
            probs_prio = None
        result['prioridad'] = str(prio_pred)
        result['prioridad_probs'] = probs_prio
    else:
        result['prioridad'] = None
        result['prioridad_probs'] = None

    if model_cat:
        cat_pred = model_cat.predict([texto])[0]
        probs_cat = None
        try:
            probs_cat = model_cat.predict_proba([texto])[0].tolist()
            classes_cat = model_cat.classes_.tolist()
            probs_cat = dict(zip(classes_cat, probs_cat))
        except Exception:
            probs_cat = None
        result['categoria'] = str(cat_pred)
        result['categoria_probs'] = probs_cat
    else:
        result['categoria'] = None
        result['categoria_probs'] = None

    return result
