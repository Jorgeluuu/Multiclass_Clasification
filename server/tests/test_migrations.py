import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from server.database.migrations import DatabaseMigration

# Test Unitario para la migración de la base de datos
def test_get_complete_student_schema_keys():
    # 1. Instancia la clase
    migration = DatabaseMigration()
    
    # 2. Llama al método que quieres testear
    schema = migration.get_complete_student_schema()
    
    # 3. Define las claves que esperas que estén en el esquema
    expected_keys = [
        'curricular_units_1st_sem_grade',
        'curricular_units_2nd_sem_grade',
        'curricular_units_1st_sem_approved',
        'curricular_units_2nd_sem_approved',
        'curricular_units_1st_sem_evaluations',
        'curricular_units_2nd_sem_evaluations',
        'unemployment_rate',
        'gdp',
        'age_at_enrollment',
        'scholarship_holder',
        'tuition_fees_up_to_date',
        'marital_status',
        'previous_qualification',
        'mothers_qualification',
        'fathers_qualification',
        'target',
        'probability_graduate',
        'probability_dropout',
        'probability_enrolled',
        'predicted_outcome',
        'confidence'
    ]
    
    for key in expected_keys:
        assert key in schema, f"Falta la clave esperada: {key}"
        assert isinstance(schema, dict)
        assert len(schema) >= 20