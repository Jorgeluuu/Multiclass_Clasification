import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
import joblib
# ---------------------------------------------------------------------------------------------------------------------
# current_dir = os.getcwd()
# parent_dir = os.path.dirname(current_dir)
# data_dir = os.path.join(parent_dir, "data")
# file_path = os.path.join(data_dir, "")
# raw_data_csv_path = os.path.join(data_dir, "raw_data.csv") # Cambiar por el archivo correcto!!!!!!!!!!!!!!!!!!!!!!!!!!!

# df_students = pd.read_csv(raw_data_csv_path) # Cambiar el nombre de la variable por el correcto!!!!!!!!!!!!!!!!!!!!!!!!

# ---------------------------------------------------------------------------------------------------------------------
# Este trozo necesita ser cambiado por el correcto, de momento no hay modelo y esto es un ejemplo!!!!!!!!!!!!!!!!!!!!!!

data = {
    'age': [18, 22, 25, 30, 35, 40],
    'education_years': [12, 14, 16, 18, 20, 22],
    'credits_failed': [0, 2, 1, 3, 0, 4],
    'target': ['Graduate', 'Enrolled', 'Dropout', 'Graduate', 'Dropout', 'Enrolled']
}

df = pd.DataFrame(data)

X = df.drop('target', axis=1)
y = df['target']

# Training a Random Forest Classifier
model = RandomForestClassifier()
model.fit(X, y)

# Save model
joblib.dump(model, 'server/models/model.pkl')
print("✅ Modelo de prueba guardado como model.pkl")