from pydantic import BaseModel, Field

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
    
    # ✅ SOLUCIÓN: Usar Field(alias=...) para aceptar nombres con apóstrofes
    mothers_qualification: str = Field(alias="mother's_qualification")
    fathers_qualification: str = Field(alias="father's_qualification")