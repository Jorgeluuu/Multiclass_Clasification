import os
import pickle
import xgboost as xgb
import pandas as pd
import numpy as np

from .preprocessing import PreprocessingPipeline
import sys
import server.models.preprocessing as preprocessing_module
sys.modules['preprocessing'] = preprocessing_module

# Rutas relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
pipeline_path = os.path.join(current_dir, "..", "data", "xgboost_multiclass_pipeline.pkl")
model_path = os.path.join(current_dir, "..", "data", "xgboost_multiclass_model.pkl")

print(f"🔍 Cargando desde:")
print(f"   Pipeline: {pipeline_path}")
print(f"   Modelo: {model_path}")

# Cargar pipeline y modelo
try:
    with open(pipeline_path, 'rb') as f:
        preprocessing_pipeline = pickle.load(f)
    print(f"✅ Pipeline cargado: {type(preprocessing_pipeline)}")
    
    with open(os.path.abspath(model_path), "rb") as f:
        model = pickle.load(f)
    print(f"✅ Modelo cargado: {type(model)}")
    
except Exception as e:
    print(f"❌ Error cargando archivos: {e}")
    raise

def predict_student_outcome(data: dict) -> str:
    """
    Función original que solo devuelve la predicción (para compatibilidad)
    """
    result = predict_student_outcome_with_probabilities(data)
    return result['prediction']

def predict_student_outcome_with_probabilities(data: dict) -> dict:
    """
    Nueva función que devuelve predicción + probabilidades reales del modelo XGBoost
    """
    print("\n" + "="*50)
    print("🎯 PREDICCIÓN CON PROBABILIDADES REALES")
    print("="*50)
    
    print(f"📥 Datos de entrada: {data}")
    print(f"✔️ Tipo de entrada: {type(data)}")

    try:
        # 1. Convertir a DataFrame
        df_input = pd.DataFrame([data])
        print(f"\n🧾 DataFrame inicial:")
        print(f"   Shape: {df_input.shape}")
        print(f"   Columns: {list(df_input.columns)}")
        print(f"   Datos: {df_input.iloc[0].to_dict()}")

        # 2. Aplicar preprocesamiento
        print(f"\n🔧 Aplicando preprocesamiento...")
        X_preprocessed = preprocessing_pipeline.transform(df_input)
        print(f"✅ Preprocesamiento completado:")
        print(f"   Shape: {X_preprocessed.shape}")
        print(f"   Columnas: {len(X_preprocessed.columns)}")
        print(f"   Suma total: {X_preprocessed.sum().sum()}")

        # 3. Verificar que no todos los valores sean 0
        if X_preprocessed.sum().sum() == 0:
            print("⚠️ ADVERTENCIA: Todos los valores son 0 después del preprocesamiento!")
            print("Esto indica un problema en el pipeline de preprocesamiento")

        # 4. Crear DMatrix y obtener probabilidades
        dmatrix = xgb.DMatrix(X_preprocessed)
        prediction_probabilities = model.predict(dmatrix)
        
        print(f"\n🔮 Probabilidades del modelo XGBoost:")
        print(f"   Shape: {prediction_probabilities.shape}")
        print(f"   Tipo: {type(prediction_probabilities)}")
        print(f"   Valores raw: {prediction_probabilities}")
        
        # 5. Extraer probabilidades y clase predicha
        probs_array = prediction_probabilities[0]  # Primera (y única) predicción
        predicted_class_idx = np.argmax(probs_array)
        
        # Mapeo de clases (debe coincidir con el entrenamiento)
        class_map = {
            0: "Dropout",
            1: "Graduate", 
            2: "Enrolled"
        }
        
        predicted_class = class_map[predicted_class_idx]
        confidence = float(probs_array[predicted_class_idx])  # Confianza = probabilidad máxima
        
        # 6. Crear diccionario de probabilidades con nombres legibles
        probabilities = {
            "Dropout": float(probs_array[0]),
            "Graduate": float(probs_array[1]),
            "Enrolled": float(probs_array[2])
        }
        
        print(f"\n🎯 Resultado detallado:")
        print(f"   Clase predicha: {predicted_class} (índice {predicted_class_idx})")
        print(f"   Confianza: {confidence:.4f} ({confidence*100:.1f}%)")
        print(f"   Probabilidades:")
        for class_name, prob in probabilities.items():
            indicator = " ← PREDICHA" if class_name == predicted_class else ""
            print(f"     {class_name}: {prob:.4f} ({prob*100:.1f}%){indicator}")
        
        # 7. Verificar que las probabilidades suman 1
        prob_sum = sum(probabilities.values())
        print(f"   Suma de probabilidades: {prob_sum:.6f}")
        
        if abs(prob_sum - 1.0) > 0.001:
            print(f"⚠️ ADVERTENCIA: Las probabilidades no suman 1.0 (suman {prob_sum:.6f})")
        
        # 8. Resultado final
        result = {
            'prediction': predicted_class,
            'probabilities': probabilities,
            'confidence': confidence,
            'model_type': 'XGBoost',
            'preprocessed_features_count': X_preprocessed.shape[1]
        }
        
        print(f"\n✅ Predicción completada exitosamente")
        return result

    except Exception as e:
        print(f"\n💥 ERROR en predictor: {e}")
        import traceback
        traceback.print_exc()
        raise