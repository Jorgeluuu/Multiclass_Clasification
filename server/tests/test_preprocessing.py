import pandas as pd
import pytest
from server.models.preprocessing import PreprocessingPipeline

# Test Unitario para el pipeline de preprocesamiento
def test_preprocessing_pipeline_transform():
    # 1. Definir las features esperadas por el modelo
    features = [
        'curricular_units_1st_sem_(grade)',
        'curricular_units_2nd_sem_(grade)',
        'curricular_units_1st_sem_(approved)',
        'curricular_units_2nd_sem_(approved)',
        'curricular_units_1st_sem_(evaluations)',
        'curricular_units_2nd_sem_(evaluations)',
        'unemployment_rate',
        'gdp',
        'age_at_enrollment',
        "mother's_qualification_Bachelor",
        "father's_qualification_Doctorate",
        'scholarship_holder_Yes',
        'marital_status_Single'
    ]

    # 2. Crear un DataFrame de entrada simulando datos crudos
    data = {
        'curricular_units_1st_sem_grade': [15.0],  
        'curricular_units_2nd_sem_grade': [14.0],  
        'curricular_units_1st_sem_approved': [5],  
        'curricular_units_2nd_sem_approved': [6],  
        'curricular_units_1st_sem_evaluations': [7],  
        'curricular_units_2nd_sem_evaluations': [8],  
        'unemployment_rate': [10.5],
        'gdp': [20000],
        'age_at_enrollment': [20],
        "mother's_qualification": ['Bachelor'],
        "father's_qualification": ['Doctorate'],
        'scholarship_holder': ['Yes'],
        'marital_status': ['Single']
    }
    df = pd.DataFrame(data)

    # 3. Instanciar el pipeline
    pipeline = PreprocessingPipeline(features=features)

    # 4. Transformar los datos
    result = pipeline.transform(df)

    # 5. Verificar que el resultado tiene las columnas esperadas y en el orden correcto
    assert list(result.columns) == features

    # 6. Verificar que los valores numéricos se han mapeado correctamente
    assert result['curricular_units_1st_sem_(grade)'].iloc[0] == 15.0
    assert result['curricular_units_2nd_sem_(grade)'].iloc[0] == 14.0

    # 7. Verificar que las columnas one-hot están correctamente codificadas
    assert result["mother's_qualification_Bachelor"].iloc[0] == 1
    assert result["father's_qualification_Doctorate"].iloc[0] == 1
    assert result['scholarship_holder_Yes'].iloc[0] == 1
    assert result['marital_status_Single'].iloc[0] == 1

    # 8. Verificar que las columnas faltantes (no presentes en el input) son 0
    for col in features:
        if col not in [
            'curricular_units_1st_sem_(grade)',
            'curricular_units_2nd_sem_(grade)',
            'curricular_units_1st_sem_(approved)',
            'curricular_units_2nd_sem_(approved)',
            'curricular_units_1st_sem_(evaluations)',
            'curricular_units_2nd_sem_(evaluations)',
            'unemployment_rate',
            'gdp',
            'age_at_enrollment',
            "mother's_qualification_Bachelor",
            "father's_qualification_Doctorate",
            'scholarship_holder_Yes',
            'marital_status_Single'
        ]:
            assert result[col].iloc[0] == 0

    # 9. Verificar que las columnas originales categóricas ya no están
    for col in [
        'scholarship_holder', 'tuition_fees_up_to_date', 'marital_status',
        'previous_qualification', "mother's_qualification", "father's_qualification"
    ]:
        assert col not in result.columns

    # 10. Verificar que el DataFrame resultante tiene una sola fila
    assert result.shape[0] == 1

# Ejecutar este test con:
# pytest server/tests/test_preprocessing.py

