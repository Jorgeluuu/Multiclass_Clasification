# server/models/predictor.py
import joblib
import pandas as pd
import os

# Ruta donde se espera que esté el modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

# Cargar el modelo solo una vez al iniciar la aplicación
try:
    _model = joblib.load(MODEL_PATH)
    print(f"✅ Modelo cargado desde {MODEL_PATH}")
except FileNotFoundError:
    print(f"❌ Error: El archivo del modelo no se encontró en {MODEL_PATH}. Asegúrate de ejecutar model_trainer.py primero.")
    _model = None # O manejar el error de otra forma, como levantar una excepción

def predict_student_outcome(age: int, education_years: int, credits_failed: int) -> str:
    """
    Realiza una predicción sobre el resultado del estudiante.
    """
    if _model is None:
        return "Error: Modelo no cargado." # O levantar un error HTTP en FastAPI

    input_data = pd.DataFrame([[age, education_years, credits_failed]],
                              columns=['age', 'education_years', 'credits_failed'])
    prediction = _model.predict(input_data)
    return prediction[0]