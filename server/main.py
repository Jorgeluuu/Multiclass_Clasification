# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from typing import Literal

# from models.predictor import predict_student_outcome
# from database.supabase_client import supabase # Importa el cliente Supabase

# # Definir un modelo de datos para las solicitudes de entrada
# class StudentInput(BaseModel):
#     age: int
#     education_years: int
#     credits_failed: int

# # Definir un modelo de datos para la respuesta de predicción
# class PredictionResponse(BaseModel):
#     prediction: Literal['Graduate', 'Enrolled', 'Dropout'] # Asumiendo estos son los resultados posibles
#     message: str

# # !!!!!!!!!!!!!!!! a cambiar cuando haya datos reales
# class StudentData(BaseModel):
#     age: int
#     education_years: int
#     credits_failed: int
#     target: str # El resultado de la predicción

# app = FastAPI(
#     title="API de Predicción de Rendimiento Estudiantil",
#     description="API para predecir el rendimiento académico de estudiantes y guardar los datos en Supabase."
# )

# # Configurar CORS para permitir solicitudes desde el frontend (React)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], # Esto permite a React conectarse desde cualquier origen. En producción, especificar dominios.
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def read_root():
#     return {"message": "🧠 API de Predicción con FastAPI - Funcionando. Usa POST en /predict para obtener predicciones."}

# @app.post("/predict", response_model=PredictionResponse)
# async def predict_student(input_data: StudentInput):
#     """
#     Realiza una predicción del rendimiento del estudiante y la guarda en Supabase.
#     """
#     try:
#         # Realizar la predicción usando el modelo de Python
#         prediction = predict_student_outcome(
#             input_data.age,
#             input_data.education_years,
#             input_data.credits_failed
#         )

#         # Si el predictor devuelve un error porque el modelo no se cargó
#         if "Error: Modelo no cargado" in prediction:
#             raise HTTPException(status_code=500, detail=prediction)

#         # Preparar los datos para Supabase, incluyendo la predicción
#         student_data_to_save = StudentData(
#             age=input_data.age,
#             education_years=input_data.education_years,
#             credits_failed=input_data.credits_failed,
#             target=prediction
#         )

#         # Guardar en Supabase
#         # !!!!!!!!!! El nombre debe de ser cambiado por el correcto cuando haya una bd real
#         response = supabase.table("Fake").insert(student_data_to_save.model_dump()).execute() 

#         if response.data:
#             print(f"✅ Datos guardados en Supabase: {response.data}")
#             return PredictionResponse(prediction=prediction, message="Predicción y datos guardados en Supabase ✅")
#         else:
#             # Aquí capturamos errores de Supabase que no sean HTTP
#             print(f"⚠️ Error al guardar en Supabase: {response.status_code} - {response.count} - {response.data} - {response.status}")
#             raise HTTPException(status_code=500, detail="Error al guardar datos en Supabase.")

#     except Exception as e:
#         print(f"❌ Error inesperado en /predict: {e}")
#         raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

# # Ruta para obtener estudiantes
# @app.get("/students")
# async def get_students():
#     """
#     Obtiene todos los estudiantes de la tabla 'Fake' de Supabase.
#     """
#     try:
#         response = supabase.table("Fake").select("*").execute()
#         if response.data:
#             return response.data
#         else:
#             raise HTTPException(status_code=500, detail="Error al obtener datos de Supabase.")
#     except Exception as e:
#         print(f"❌ Error al obtener estudiantes de Supabase: {e}")
#         raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")


from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from server.models.predictor import predict_student_outcome
from .database.supabase_client import supabase  # Supabase client
from server.models.preprocessing import PreprocessingPipeline

import os
from dotenv import load_dotenv
# Carga el .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Añade la raíz del proyecto al PYTHONPATH
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
print("SSL_CERT_FILE:", os.environ.get("SSL_CERT_FILE"))

# Define aquí los features reales que espera tu pipeline
class StudentInput(BaseModel):
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

class PredictionResponse(BaseModel):
    prediction: str 
    message: str

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

app = FastAPI(
    title="API de Predicción Estudiantil con XGBoost",
    description="API para predecir rendimiento académico usando un modelo entrenado.",
)

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
    return {"message": "✅ API corriendo. Usa /predict para predicciones."}

@app.post("/predict", response_model=PredictionResponse)
async def predict_student(input_data: StudentInput):
    try:
        prediction = predict_student_outcome(input_data)

        if isinstance(prediction, str) and "Error" in prediction:
            raise HTTPException(status_code=500, detail=prediction)

        # Prepara para guardar en Supabase
        student_data = StudentData(**input_data.dict(), target=prediction)

        # Cambia 'Fake' por el nombre real de tu tabla
        response = supabase.table("students").insert(student_data.model_dump()).execute()

        if response.data:
            print(f"✅ Datos guardados en Supabase: {response.data}")
            return PredictionResponse(prediction=prediction, message="Predicción y datos guardados en Supabase ✅")
        
        else:
            print(f"⚠️ Error al guardar en Supabase: {response.status_code} - {response.count} - {response.data} - {response.status}")
    except Exception as e:
        print(f"❌ Error inesperado en /predict: {e}")
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")

@app.get("/students")
async def get_students():
    try:
        response = supabase.table("students").select("*").execute()
        if response.data:
            return response.data
        else:
            raise HTTPException(status_code=500, detail="❌ No se pudo obtener estudiantes.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error: {e}")
