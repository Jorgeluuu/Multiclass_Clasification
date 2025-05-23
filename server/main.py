from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from server.models.predictor import predict_student_outcome
from .database.supabase_client import supabase  # Supabase client
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
    description="API para predecir rendimiento académico usando un modelo entrenado."
)
#------------------------------

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
    
      // GET request
 useEffect(() => {axios.get('http://localhost:8000/api/data').then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);
# -----------------------------

dist_path = os.path.join(os.path.dirname(__file__), '..', 'client', 'dist'),
app.mount("/assets", StaticFiles(directory=os.path.join(dist_path, 'assets')), name="assets")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(dist_path, 'index.html'))