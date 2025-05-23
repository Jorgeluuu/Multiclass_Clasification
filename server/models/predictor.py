
# -------------------------------------------------------------------------------------------------------
# server/models/predictor.py
import os
import pickle
import xgboost as xgb
import pandas as pd

from .preprocessing import PreprocessingPipeline  # Necesario para deserializar el pipeline
# from server.models.preprocessing import PreprocessingPipeline
import sys
import server.models.preprocessing as preprocessing_module
sys.modules['preprocessing'] = preprocessing_module


# Rutas relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
pipeline_path = os.path.join(current_dir, "..", "data", "xgboost_multiclass_pipeline.pkl")
model_path = os.path.join(current_dir, "..", "data", "xgboost_multiclass_model.pkl")



# Cargar pipeline y modelo
with open(pipeline_path, 'rb') as f:
    preprocessing_pipeline = pickle.load(f)

print(type(preprocessing_pipeline))
print(preprocessing_pipeline.__class__.__module__)

with open(os.path.abspath(model_path), "rb") as f:
    model = pickle.load(f)

def predict_student_outcome(data: dict) -> str:
    print("📥 Entrada cruda dict:", data)
    print("✔️ Es dict:", isinstance(data, dict))

    try:
        df_input = pd.DataFrame([data])
        print("🧾 DataFrame:")
        print(df_input)

        X_preprocessed = preprocessing_pipeline.transform(df_input)
        print("🔧 Preprocesado:")
        print(X_preprocessed)

        dmatrix = xgb.DMatrix(X_preprocessed)
        prediction_probs = model.predict(dmatrix)
        predicted_class = prediction_probs.argmax(axis=1)[0]

        class_map = {
            0: "Dropout",
            1: "Graduate",
            2: "Enrolled"
        }

        return class_map[predicted_class]

    except Exception as e:
        print(f"💥 ERROR en predictor: {e}")
        raise