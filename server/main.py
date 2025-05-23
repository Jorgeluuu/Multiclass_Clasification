from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Dict, Optional
from server.models.predictor import predict_student_outcome_with_probabilities  # ✅ Nueva función
from .database.supabase_client import supabase
from server.models.preprocessing import PreprocessingPipeline
from server.models.schemas import StudentInput

import os
from dotenv import load_dotenv

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ---------------------------
# Carga el .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Añade la raíz del proyecto al PYTHONPATH
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
print("SSL_CERT_FILE:", os.environ.get("SSL_CERT_FILE"))

# ✅ RESPONSE MODEL ACTUALIZADO CON PROBABILIDADES
class PredictionResponse(BaseModel):
    prediction: str 
    probabilities: Dict[str, float]  # ✅ Probabilidades reales del modelo
    confidence: float                # ✅ Confianza (probabilidad máxima)
    message: str
    model_type: Optional[str] = "XGBoost"  # ✅ Tipo de modelo

class StudentData(BaseModel):
    curricular_units_1st_sem_grade: float
    curricular_units_2nd_sem_grade: float
    curricular_units_1st_sem_approved: int
    curricular_units_2nd_sem_approved: int
    curricular_units_1st_sem_evaluations: int
    curricular_units_2nd_sem_evaluations: int
    unemployment_rate: float
    gdp: float
    age_at_enrollment: int

    scholarship_holder: str
    tuition_fees_up_to_date: str
    marital_status: str
    previous_qualification: str
    mothers_qualification: str
    fathers_qualification: str

    target: str
    
    # ✅ NUEVOS CAMPOS PARA PROBABILIDADES INDIVIDUALES
    probability_graduate: Optional[float] = None
    probability_dropout: Optional[float] = None
    probability_enrolled: Optional[float] = None
    predicted_outcome: Optional[str] = None
    confidence: Optional[float] = None

app = FastAPI(
    title="API de Predicción Estudiantil con XGBoost",
    description="API para predecir rendimiento académico usando un modelo entrenado con probabilidades reales."
)

# ----------    
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajusta esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "✅ API corriendo. Usa /predict para predicciones con probabilidades reales."}

@app.post("/predict", response_model=PredictionResponse)
async def predict_student(input_data: StudentInput):
    """
    Endpoint para predicción académica con probabilidades reales del modelo XGBoost
    ✅ SOLO MODELO ML - SIN RESPALDO
    """
    try:
        print(f"\n🎯 Nueva solicitud de predicción:")
        print(f"   Datos recibidos: {input_data.dict()}")
        
        # ✅ USAR FUNCIÓN MEJORADA QUE DEVUELVE PROBABILIDADES REALES
        try:
            print("🔮 Llamando al modelo XGBoost...")
            prediction_result = predict_student_outcome_with_probabilities(input_data.dict())
            print(f"✅ Resultado completo del modelo ML: {prediction_result}")
            
            prediction = prediction_result['prediction']
            probabilities = prediction_result['probabilities']
            confidence = prediction_result['confidence']
            model_type = prediction_result.get('model_type', 'XGBoost')
            
            print(f"🎯 Predicción: {prediction}")
            print(f"📊 Probabilidades: {probabilities}")
            print(f"🎯 Confianza: {confidence:.4f}")
            
        except Exception as predictor_error:
            print(f"❌ Error crítico en modelo ML: {predictor_error}")
            # ✅ NO HAY RESPALDO - Error directo
            raise HTTPException(
                status_code=500, 
                detail=f"Error en el modelo de predicción XGBoost: {str(predictor_error)}"
            )

        # ✅ VALIDACIONES ESTRICTAS
        valid_predictions = ["Graduate", "Dropout", "Enrolled"]
        if prediction not in valid_predictions:
            raise HTTPException(
                status_code=500,
                detail=f"Predicción inválida del modelo: {prediction}. Esperado: {valid_predictions}"
            )

        # Validar probabilidades
        if not probabilities or not isinstance(probabilities, dict):
            raise HTTPException(
                status_code=500,
                detail="El modelo no devolvió probabilidades válidas"
            )
        
        # Verificar que las probabilidades suman aproximadamente 1.0
        prob_sum = sum(probabilities.values())
        if abs(prob_sum - 1.0) > 0.01:
            print(f"⚠️ ADVERTENCIA: Probabilidades suman {prob_sum:.6f} en lugar de 1.0")
        
        # Verificar que la confianza está en rango válido
        if not (0.0 <= confidence <= 1.0):
            raise HTTPException(
                status_code=500,
                detail=f"Confianza inválida: {confidence}. Debe estar entre 0.0 y 1.0"
            )

        # ✅ GUARDAR EN SUPABASE CON PROBABILIDADES INDIVIDUALES
        try:
            # Crear datos base del estudiante
            student_data_dict = input_data.dict()
            student_data_dict['target'] = prediction
            
            # ✅ AGREGAR PROBABILIDADES INDIVIDUALES para que el frontend las encuentre
            student_data_dict['probability_graduate'] = probabilities.get('Graduate', 0.0)
            student_data_dict['probability_dropout'] = probabilities.get('Dropout', 0.0) 
            student_data_dict['probability_enrolled'] = probabilities.get('Enrolled', 0.0)
            student_data_dict['predicted_outcome'] = prediction  # Campo adicional
            student_data_dict['confidence'] = confidence
            
            print(f"💾 Datos para guardar en Supabase:")
            print(f"   probability_graduate: {student_data_dict['probability_graduate']}")
            print(f"   probability_dropout: {student_data_dict['probability_dropout']}")
            print(f"   probability_enrolled: {student_data_dict['probability_enrolled']}")
            
            # Crear objeto StudentData extendido
            student_data = StudentData(**student_data_dict)
            response = supabase.table("students").insert(student_data.model_dump()).execute()
            
            if response.data:
                print(f"✅ Datos guardados en Supabase: ID {response.data[0].get('id', 'N/A')}")
                success_message = f"Predicción XGBoost realizada (confianza: {confidence:.1%}) y datos guardados ✅"
            else:
                print(f"⚠️ Error al guardar en Supabase: {response}")
                success_message = f"Predicción XGBoost realizada (confianza: {confidence:.1%}) pero error al guardar ⚠️"
                
        except Exception as db_error:
            print(f"⚠️ Error en base de datos: {db_error}")
            success_message = f"Predicción XGBoost realizada (confianza: {confidence:.1%}) pero error al guardar en BD ⚠️"

        # ✅ RESPUESTA CON PROBABILIDADES REALES
        return PredictionResponse(
            prediction=prediction,
            probabilities=probabilities,
            confidence=confidence,
            message=success_message,
            model_type=model_type
        )
            
    except HTTPException:
        # Re-lanzar errores HTTP sin modificar
        raise
    except Exception as e:
        print(f"❌ Error inesperado en /predict: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno del servidor en predicción: {str(e)}"
        )

@app.get("/students")
async def get_students():
    """
    Endpoint para obtener todos los estudiantes/predicciones guardadas
    """
    try:
        print("📋 Obteniendo lista de estudiantes...")
        response = supabase.table("students").select("*").execute()
        
        if response.data:
            print(f"✅ Obtenidos {len(response.data)} registros de estudiantes")
            return response.data
        else:
            print("⚠️ No se encontraron estudiantes en la base de datos")
            raise HTTPException(
                status_code=404, 
                detail="No se encontraron registros de estudiantes"
            )
            
    except HTTPException:
        # Re-lanzar errores HTTP
        raise
    except Exception as e:
        print(f"❌ Error obteniendo estudiantes: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al obtener estudiantes: {str(e)}"
        )

# ✅ ENDPOINT ADICIONAL PARA VERIFICAR ESTADO DEL MODELO
@app.get("/model/status")
async def model_status():
    """
    Endpoint para verificar el estado del modelo y pipeline
    """
    try:
        from server.models.predictor import preprocessing_pipeline, model
        
        # Verificar que el modelo y pipeline están cargados
        model_loaded = model is not None
        pipeline_loaded = preprocessing_pipeline is not None
        
        # Información del modelo
        model_info = {
            "model_loaded": model_loaded,
            "pipeline_loaded": pipeline_loaded,
            "model_type": "XGBoost" if model_loaded else None,
            "pipeline_type": type(preprocessing_pipeline).__name__ if pipeline_loaded else None
        }
        
        if model_loaded and pipeline_loaded:
            # Hacer una predicción de prueba para verificar funcionamiento
            test_data = {
                'curricular_units_1st_sem_grade': 15.0,
                'curricular_units_2nd_sem_grade': 14.0,
                'curricular_units_1st_sem_approved': 5,
                'curricular_units_2nd_sem_approved': 4,
                'curricular_units_1st_sem_evaluations': 6,
                'curricular_units_2nd_sem_evaluations': 5,
                'unemployment_rate': 10.0,
                'gdp': 1.5,
                'age_at_enrollment': 20,
                'scholarship_holder': 'Yes',
                'tuition_fees_up_to_date': 'Yes',
                'marital_status': 'Single',
                'previous_qualification': 'Secondary education',
                'mothers_qualification': 'Higher education—bachelor\'s degree',
                'fathers_qualification': 'Secondary education—12th year of schooling or equivalent'
            }
            
            try:
                test_result = predict_student_outcome_with_probabilities(test_data)
                model_info["test_prediction"] = {
                    "success": True,
                    "prediction": test_result['prediction'],
                    "confidence": test_result['confidence']
                }
            except Exception as test_error:
                model_info["test_prediction"] = {
                    "success": False,
                    "error": str(test_error)
                }
        
        return {
            "status": "healthy" if model_loaded and pipeline_loaded else "unhealthy",
            "model_info": model_info,
            "message": "Modelo y pipeline funcionando correctamente" if model_loaded and pipeline_loaded else "Problema con modelo o pipeline"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Error verificando estado del modelo"
        }