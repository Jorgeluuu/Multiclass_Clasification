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
      // Nombres exactos que espera el backend según schemas.py
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
      // ✅ Mantener nombres sin apóstrofe para el backend
      mothers_qualification: formData.mothers_qualification || formData["mother's_qualification"],
      fathers_qualification: formData.fathers_qualification || formData["father's_qualification"]
    };
    
    console.log('✅ Datos convertidos para backend:', backendData);
    
    // Verificar que no hay valores undefined o null
    for (const [key, value] of Object.entries(backendData)) {
      if (value === undefined || value === null || value === '') {
        console.warn(`⚠️ Valor problemático para ${key}:`, value);
      }
    }
    
    return backendData;
  },

  /**
   * Realiza una predicción basada en los datos del estudiante
   * ✅ SOLO USA EL MODELO - SIN RESPALDO NI SIMULACIONES
   * @param {Object} studentData - Datos del estudiante para la predicción
   * @returns {Promise} - Promesa que resuelve con el resultado de la predicción
   */
  predictOutcome: async (studentData) => {
    try {
      console.log('📤 Enviando datos originales:', studentData);
      
      // Convertir datos al formato del backend
      const backendData = studentService.convertToBackendFormat(studentData);
      console.log('📤 Enviando datos convertidos al backend:', backendData);
      
      const response = await axios.post(`${API_URL}/predict`, backendData);
      console.log('📥 Respuesta completa del backend:', response.data);
      
      // ✅ VALIDACIÓN ESTRICTA: Solo aceptar respuestas del modelo ML
      if (!response.data.prediction) {
        throw new Error('El backend no devolvió una predicción válida del modelo ML');
      }
      
      const prediction = response.data.prediction;
      console.log('🎯 Predicción del modelo:', prediction);
      
      // ✅ VERIFICAR que la predicción es válida
      const validPredictions = ['Graduate', 'Dropout', 'Enrolled'];
      if (!validPredictions.includes(prediction)) {
        throw new Error(`Predicción inválida del modelo: ${prediction}. Debe ser una de: ${validPredictions.join(', ')}`);
      }
      
      // ✅ USAR PROBABILIDADES REALES DEL MODELO
      let probabilities = null;
      let confidence = null;
      
      if (response.data.probabilities) {
        // Probabilidades reales del modelo XGBoost
        probabilities = response.data.probabilities;
        confidence = response.data.confidence;
        console.log('📊 Probabilidades del modelo XGBoost:', probabilities);
        console.log('🎯 Confianza del modelo:', confidence);
        
        // Verificar que las probabilidades son válidas
        const probSum = Object.values(probabilities).reduce((sum, prob) => sum + prob, 0);
        if (Math.abs(probSum - 1.0) > 0.01) {
          console.warn(`⚠️ Las probabilidades no suman 1.0: ${probSum}`);
        }
        
        // Verificar que la predicción coincide con la probabilidad máxima
        const maxProbClass = Object.keys(probabilities).reduce((a, b) => 
          probabilities[a] > probabilities[b] ? a : b
        );
        if (maxProbClass !== prediction) {
          console.warn(`⚠️ Inconsistencia: predicción=${prediction}, max_prob_class=${maxProbClass}`);
        }
        
      } else {
        // Si no hay probabilidades, informar que faltan
        console.warn('⚠️ El backend no devolvió probabilidades del modelo');
        console.log('💡 Recomendación: Verificar que el backend esté usando la nueva función con probabilidades');
      }
      
      return {
        prediction: prediction,
        probabilities: probabilities, // Probabilidades reales del XGBoost o null
        confidence: confidence,       // Confianza real del modelo o null
        message: response.data.message,
        isFromModel: true,           // Confirmamos que viene del modelo
        hasRealProbabilities: probabilities !== null,
        modelType: response.data.model_type || 'XGBoost'
      };
      
    } catch (error) {
      // Manejo de errores centralizado - SIN RESPALDO
      console.error('❌ Error realizando la predicción:', error);
      
      let errorMessage = 'Error al realizar la predicción con el modelo ML';
      
      if (error.response) {
        console.error('❌ Error response:', error.response.data);
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status} del modelo`;
      } else if (error.request) {
        console.error('❌ Error request:', error.request);
        errorMessage = 'No se pudo conectar con el modelo ML. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
      } else {
        console.error('❌ Error config:', error.message);
        errorMessage = `Error en la comunicación con el modelo: ${error.message}`;
      }
      
      // ✅ NO HAY RESPALDO - Si falla el modelo, falla la predicción
      throw new Error(errorMessage);
    }
  },

  /**
   * Obtiene todas las predicciones realizadas
   * NOTA: El backend actual tiene /students, no /predictions
   * @param {Object} params - Parámetros de consulta (limit, offset, filter)
   * @returns {Promise} - Promesa que resuelve con el listado de predicciones
   */
  getAllPredictions: async (params = {}) => {
    try {
      const { limit = 100, offset = 0, outcome_filter = null } = params;
      
      console.log('📤 Obteniendo predicciones con params:', { limit, offset, outcome_filter });
      
      // Usar el endpoint /students que existe en el backend
      const response = await axios.get(`${API_URL}/students`);
      console.log('📥 Respuesta de estudiantes:', response.data);
      
      // Simular paginación y filtrado en el frontend ya que el backend no lo soporta
      let data = response.data || [];
      
      // Filtrar por outcome si se especifica
      if (outcome_filter) {
        data = data.filter(item => 
          item.predicted_outcome === outcome_filter || 
          item.target === outcome_filter
        );
        console.log(`🔍 Filtrado por ${outcome_filter}, quedaron ${data.length} registros`);
      }
      
      // Simular paginación
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
        console.error('❌ Error response:', error.response.data);
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        console.error('❌ Error request:', error.request);
        errorMessage = 'No se recibió respuesta del servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
      } else {
        console.error('❌ Error config:', error.message);
        errorMessage = error.message;
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Obtiene una predicción específica por ID
   * @param {number} predictionId - ID de la predicción
   * @returns {Promise} - Promesa que resuelve con los datos de la predicción
   */
  getPredictionById: async (predictionId) => {
    try {
      console.log(`📤 Obteniendo predicción ID: ${predictionId}`);
      
      // Como el backend no tiene endpoint específico, obtenemos todas y filtramos
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
   * Adaptado para trabajar con la estructura del backend existente
   * @param {Object} predictionData - Datos de la predicción desde la BD
   * @returns {Object} - Datos en formato del formulario
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
      // Mapear nombres del backend (sin apóstrofe) al formulario
      mothers_qualification: predictionData.mothers_qualification || predictionData["mother's_qualification"] || '',
      fathers_qualification: predictionData.fathers_qualification || predictionData["father's_qualification"] || ''
    };
    
    console.log('✅ Datos convertidos para formulario:', formData);
    
    return formData;
  }
};

export default studentService;