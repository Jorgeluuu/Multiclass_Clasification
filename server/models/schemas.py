from pydantic import BaseModel

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
