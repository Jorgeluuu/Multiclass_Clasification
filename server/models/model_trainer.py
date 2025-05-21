import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
# -------------------------------------------------------------------------------------------------------

# current_dir = os.path.dirname(os.path.abspath(__file__))
# server_dir = os.path.dirname(current_dir)
# project_root_dir = os.path.dirname(server_dir)
# data_dir = os.path.join(project_root_dir, "data")
# csv_file_path = os.path.join(data_dir, "for_trying_model.csv") # Cambiará cuando haya otro CSV

# model_save_path = os.path.join(current_dir, "model.pkl")

# -------------------------------------------------------------------------------------------------------
# # DATOS FAKE PARA TESTEAR EL BACK
data = {
    'age': [18, 22, 25, 30, 35, 40],
    'education_years': [12, 14, 16, 18, 20, 22],
    'credits_failed': [0, 2, 1, 3, 0, 4],
    'target': ['Graduate', 'Enrolled', 'Dropout', 'Graduate', 'Dropout', 'Enrolled']
}

df = pd.DataFrame(data)

X = df.drop('target', axis=1)
y = df['target']
# -------------------------------------------------------------------------------------------------------
# Entrenar el modelo
model = RandomForestClassifier(random_state=42) # Añadir random_state para reproducibilidad
model.fit(X, y)
# -------------------------------------------------------------------------------------------------------
# El pkl se guarda en la misma carpeta que este script
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
joblib.dump(model, model_path)
print(f"✅ Modelo de prueba guardado como {model_path}")