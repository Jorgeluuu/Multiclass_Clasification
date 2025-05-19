import sys
import json
import joblib
import pandas as pd
# ---------------------------------------------------------------------------------------------------------------------
# Cargar el modelo entrenado
model = joblib.load('server/models/model.pkl')

# Recibir datos del backend
input_json = sys.argv[1]
input_data = json.loads(input_json)

# Convertir a DataFrame (debe tener las columnas correctas)
df_input = pd.DataFrame([input_data])

# Predecir
prediction = model.predict(df_input)

# Imprimir resultado
print(prediction[0])