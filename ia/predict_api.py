from flask import Flask, request, jsonify
import joblib
from pathlib import Path

app = Flask(__name__)

MODEL_PATH = Path(__file__).resolve().parent / "models" / "model.joblib"

# Cargar el modelo una sola vez al iniciar
def load_model():
    if MODEL_PATH.exists():
        print("✅ Modelo encontrado, cargando...")
        return joblib.load(MODEL_PATH)
    else:
        print("⚠️ No se encontró el modelo. Ejecuta primero ia/train_model.py")
        return None

model = load_model()

@app.route("/predict", methods=["POST"])
def predict():
    if not model:
        return jsonify({"error": "Modelo no cargado"}), 500

    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Falta el campo 'text' en el JSON"}), 400

    text = data["text"]
    prediction = model.predict([text])[0]
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    print("🚀 API de predicción iniciada en http://127.0.0.1:5000/predict")
    app.run(host="127.0.0.1", port=5000, debug=True)
