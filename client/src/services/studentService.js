import axios from 'axios';

// URL base de la API (usando variable de entorno correcta o fallback)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Servicio para predicciones académicas
const studentService = {
  /**
   * Convierte los datos del formulario frontend al formato que espera el backend
   * @param {Object} formData - Datos del formulario
   * @returns {Object} - Datos en formato del backend
   */
  convertToBackendFormat: (formData) => {
    console.log('🔄 Convirtiendo datos del formulario:', formData);
    
    const backendData = {
      curricular_units_1st_sem_grade: parseFloat(formData.curricular_units_1st_sem_grade),
      curricular_units_2nd_sem_grade: parseFloat(formData.curricular_units_2nd_sem_grade),
      curricular_units_1st_sem_approved: parseInt(formData.curricular_units_1st_sem_approved),
      curricular_units_2nd_sem_approved: parseInt(formData.curricular_units_2nd_sem_approved),
      curricular_units_1st_sem_evaluations: parseInt(formData.curricular_units_1st_sem_evaluations),
      curricular_units_2nd_sem_evaluations: parseInt(formData.curricular_units_2nd_sem_evaluations),
      unemployment_rate: parseFloat(formData.unemployment_rate),
      gdp: parseFloat(formData.gdp),
      age_at_enrollment: parseInt(formData.age_at_enrollment),
      scholarship_holder: formData.scholarship_holder,
      tuition_fees_up_to_date: formData.tuition_fees_up_to_date,
      marital_status: formData.marital_status,
      previous_qualification: formData.previous_qualification,
      "mother's_qualification": formData.mothers_qualification || formData["mother's_qualification"],
      "father's_qualification": formData.fathers_qualification || formData["father's_qualification"]
    };
    
    console.log('✅ Datos convertidos para backend:', backendData);
    
    for (const [key, value] of Object.entries(backendData)) {
      if (value === undefined || value === null || value === '') {
        console.warn(`⚠️ Valor problemático para ${key}:`, value);
      }
    }
    
    return backendData;
  },

  /**
   * Procesa la respuesta del backend (tanto POST /predict como PUT /students/{id})
   * @param {Object} responseData - Respuesta del backend
   * @param {boolean} isUpdate - Si es una actualización
   * @returns {Object} - Objeto de resultado estandarizado
   */
  processBackendResponse: (responseData, isUpdate = false) => {
    console.log('🔄 Procesando respuesta del backend:', responseData);
    
    let prediction, probabilities, confidence, message;
    
    if (isUpdate) {
      // Para actualizaciones, los datos están en 'updated'
      const updatedData = responseData.updated || responseData;
      prediction = updatedData.predicted_outcome || updatedData.target;
      probabilities = {
        'Graduate': updatedData.probability_graduate || 0,
        'Dropout': updatedData.probability_dropout || 0,
        'Enrolled': updatedData.probability_enrolled || 0
      };
      confidence = updatedData.confidence || null;
      message = responseData.message || `Predicción actualizada: ${prediction}`;
    } else {
      // Para nuevas predicciones, los datos están directamente en la respuesta
      prediction = responseData.prediction;
      probabilities = responseData.probabilities || null;
      confidence = responseData.confidence || null;
      message = responseData.message;
    }
    
    // Validar que tenemos una predicción válida
    const validPredictions = ['Graduate', 'Dropout', 'Enrolled'];
    if (!validPredictions.includes(prediction)) {
      throw new Error(`Predicción inválida: ${prediction}. Debe ser una de: ${validPredictions.join(', ')}`);
    }
    
    return {
      success: true,
      prediction: prediction,
      probabilities: probabilities,
      confidence: confidence,
      message: message,
      isUpdate: isUpdate,
      isFromModel: true,
      hasRealProbabilities: probabilities !== null,
      modelType: responseData.model_type || 'XGBoost'
    };
  },

  /**
   * Realiza una predicción basada en los datos del estudiante
   */
  predictOutcome: async (studentData) => {
    try {
      console.log('📤 Enviando datos originales:', studentData);
      const backendData = studentService.convertToBackendFormat(studentData);
      console.log('📤 Enviando datos convertidos al backend:', backendData);
      
      const response = await axios.post(`${API_URL}/predict`, backendData);
      console.log('📥 Respuesta completa del backend:', response.data);
      
      if (!response.data.prediction) {
        throw new Error('El backend no devolvió una predicción válida del modelo ML');
      }
      
      return studentService.processBackendResponse(response.data, false);
      
    } catch (error) {
      console.error('❌ Error realizando la predicción:', error);
      
      let errorMessage = 'Error al realizar la predicción con el modelo ML';
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se pudo conectar con el modelo ML. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
      } else {
        errorMessage = `Error en la comunicación con el modelo: ${error.message}`;
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Actualiza una predicción existente por ID
   */
  updatePrediction: async (id, studentData) => {
    try {
      const backendData = studentService.convertToBackendFormat(studentData);
      console.log(`📤 Actualizando predicción ID ${id}:`, backendData);
      
      const response = await axios.put(`${API_URL}/students/${id}`, backendData);
      console.log('📥 Respuesta completa de actualización:', response.data);
      
      // ✅ Usar el mismo procesador que para nuevas predicciones
      return studentService.processBackendResponse(response.data, true);
      
    } catch (error) {
      console.error('❌ Error al actualizar:', error);
      
      let errorMessage = "No se pudo actualizar la predicción. Intenta de nuevo.";
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || errorMessage;
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Obtiene todas las predicciones realizadas
   */
  getAllPredictions: async (params = {}) => {
    try {
      const { limit = 100, offset = 0, outcome_filter = null } = params;
      
      console.log('📤 Obteniendo predicciones con params:', { limit, offset, outcome_filter });
      
      const response = await axios.get(`${API_URL}/students`);
      console.log('📥 Respuesta de estudiantes:', response.data);
      
      let data = response.data || [];
      
      if (outcome_filter) {
        data = data.filter(item =>
          item.predicted_outcome === outcome_filter || 
          item.target === outcome_filter
        );
        console.log(`🔍 Filtrado por ${outcome_filter}, quedaron ${data.length} registros`);
      }
      
      const total = data.length;
      const startIndex = offset;
      const endIndex = offset + limit;
      const paginatedData = data.slice(startIndex, endIndex);
      
      console.log(`📄 Paginación: ${startIndex}-${endIndex} de ${total} registros`);
      
      return {
        data: paginatedData,
        total: total,
        page: Math.floor(offset / limit) + 1,
        totalPages: Math.ceil(total / limit),
        limit: limit,
        offset: offset
      };
    } catch (error) {
      console.error('❌ Error obteniendo predicciones:', error);
      
      let errorMessage = 'Error al obtener el listado de predicciones';
      
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
      } else {
        errorMessage = error.message;
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Obtiene una predicción específica por ID
   */
  getPredictionById: async (predictionId) => {
    try {
      console.log(`📤 Obteniendo predicción ID: ${predictionId}`);
      
      const allPredictions = await studentService.getAllPredictions();
      const prediction = allPredictions.data.find(p => p.id === predictionId);
      
      if (!prediction) {
        throw new Error('Predicción no encontrada');
      }
      
      console.log('📥 Predicción encontrada:', prediction);
      return prediction;
    } catch (error) {
      console.error('❌ Error obteniendo predicción:', error);
      
      let errorMessage = 'Error al obtener la predicción';
      
      if (error.message === 'Predicción no encontrada') {
        errorMessage = 'Predicción no encontrada';
      } else if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor';
      } else {
        errorMessage = error.message;
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Convierte los datos de la base de datos al formato del formulario
   */
  convertToFormFormat: (predictionData) => {
    console.log('🔄 Convirtiendo datos de BD a formulario:', predictionData);
    
    const formData = {
      age_at_enrollment: predictionData.age_at_enrollment?.toString() || '',
      marital_status: predictionData.marital_status || '',
      curricular_units_1st_sem_grade: predictionData.curricular_units_1st_sem_grade?.toString() || '',
      curricular_units_1st_sem_approved: predictionData.curricular_units_1st_sem_approved?.toString() || '',
      curricular_units_1st_sem_evaluations: predictionData.curricular_units_1st_sem_evaluations?.toString() || '',
      curricular_units_2nd_sem_grade: predictionData.curricular_units_2nd_sem_grade?.toString() || '',
      curricular_units_2nd_sem_approved: predictionData.curricular_units_2nd_sem_approved?.toString() || '',
      curricular_units_2nd_sem_evaluations: predictionData.curricular_units_2nd_sem_evaluations?.toString() || '',
      unemployment_rate: predictionData.unemployment_rate?.toString() || '',
      gdp: predictionData.gdp?.toString() || '',
      scholarship_holder: predictionData.scholarship_holder || '',
      tuition_fees_up_to_date: predictionData.tuition_fees_up_to_date || '',
      previous_qualification: predictionData.previous_qualification || '',
      mothers_qualification: predictionData["mother's_qualification"] || predictionData.mothers_qualification || '',
      fathers_qualification: predictionData["father's_qualification"] || predictionData.fathers_qualification || ''
    };
    
    console.log('✅ Datos convertidos para formulario:', formData);
    return formData;
  }
};

export default studentService;