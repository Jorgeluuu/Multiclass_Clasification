import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from server.models.predictor import predict_student_outcome_with_probabilities

def test_predict_student_outcome_with_probabilities():
    # 1. Simula datos de entrada válidos (ajusta los campos según tu modelo)
    data = {
        'curricular_units_1st_sem_grade': 15.0,
        'curricular_units_2nd_sem_grade': 14.0,
        'curricular_units_1st_sem_approved': 5,
        'curricular_units_2nd_sem_approved': 6,
        'curricular_units_1st_sem_evaluations': 7,
        'curricular_units_2nd_sem_evaluations': 8,
        'unemployment_rate': 10.5,
        'gdp': 20000,
        'age_at_enrollment': 20,
        "mother's_qualification": 'Bachelor',
        "father's_qualification": 'Doctorate',
        'scholarship_holder': 'Yes',
        'marital_status': 'Single'
    }

    # 2. Ejecuta la predicción
    result = predict_student_outcome_with_probabilities(data)

    # 3. Verifica la estructura del resultado
    assert isinstance(result, dict)
    assert 'prediction' in result
    assert 'probabilities' in result
    assert 'confidence' in result
    assert 'model_type' in result

    # 4. Verifica que la predicción sea una de las clases esperadas
    assert result['prediction'] in ['Dropout', 'Graduate', 'Enrolled']

    # 5. Verifica que las probabilidades suman aproximadamente 1
    prob_sum = sum(result['probabilities'].values())
    assert abs(prob_sum - 1.0) < 0.01

    # 6. Verifica que la confianza corresponde a la probabilidad máxima
    max_prob = max(result['probabilities'].values())
    assert abs(result['confidence'] - max_prob) < 1e-6

# Ejecuta este test con:
# pytest server/tests/test_predictor.py