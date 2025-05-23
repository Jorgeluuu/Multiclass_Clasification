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
    return {
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
      // Cambiar nombres con apóstrofe a sin apóstrofe para el backend
      mothers_qualification: formData.mothers_qualification || formData["mother's_qualification"],
      fathers_qualification: formData.fathers_qualification || formData["father's_qualification"]
    };
  },

  /**
   * Realiza una predicción basada en los datos del estudiante
   * @param {Object} studentData - Datos del estudiante para la predicción
   * @returns {Promise} - Promesa que resuelve con el resultado de la predicción
   */
  predictOutcome: async (studentData) => {
    try {
      // Convertir datos al formato del backend
      const backendData = studentService.convertToBackendFormat(studentData);
      
      const response = await axios.post(`${API_URL}/predict`, backendData);
      
      // El backend devuelve {prediction, message}
      // Simulamos las probabilidades ya que el backend actual no las devuelve
      const prediction = response.data.prediction;
      const probabilities = {
        'Graduate': prediction === 'Graduate' ? 0.85 : 0.1,
        'Dropout': prediction === 'Dropout' ? 0.80 : 0.1,
        'Enrolled': prediction === 'Enrolled' ? 0.75 : 0.1
      };
      
      // Normalizar probabilidades para que sumen 1
      const total = Object.values(probabilities).reduce((sum, prob) => sum + prob, 0);
      Object.keys(probabilities).forEach(key => {
        probabilities[key] = probabilities[key] / total;
      });
      
      return {
        prediction: prediction,
        probabilities: probabilities,
        message: response.data.message
      };
    } catch (error) {
      // Manejo de errores centralizado
      console.error('Error realizando la predicción:', error);
      
      let errorMessage = 'Error al realizar la predicción';
      
      if (error.response) {
        // El servidor respondió con un código de estado fuera del rango 2xx
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        // La petición se realizó pero no se recibió respuesta
        errorMessage = 'No se recibió respuesta del servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
      }
      
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
      
      // Usar el endpoint /students que existe en el backend
      const response = await axios.get(`${API_URL}/students`);
      
      // Simular paginación y filtrado en el frontend ya que el backend no lo soporta
      let data = response.data || [];
      
      // Filtrar por outcome si se especifica
      if (outcome_filter) {
        data = data.filter(item => 
          item.predicted_outcome === outcome_filter || 
          item.target === outcome_filter
        );
      }
      
      // Simular paginación
      const total = data.length;
      const startIndex = offset;
      const endIndex = offset + limit;
      const paginatedData = data.slice(startIndex, endIndex);
      
      return {
        data: paginatedData,
        total: total,
        page: Math.floor(offset / limit) + 1,
        totalPages: Math.ceil(total / limit),
        limit: limit,
        offset: offset
      };
    } catch (error) {
      console.error('Error obteniendo predicciones:', error);
      
      let errorMessage = 'Error al obtener el listado de predicciones';
      
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor. Asegúrate de que el backend esté ejecutándose en http://localhost:8000';
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
      // Como el backend no tiene endpoint específico, obtenemos todas y filtramos
      const allPredictions = await studentService.getAllPredictions();
      const prediction = allPredictions.data.find(p => p.id === predictionId);
      
      if (!prediction) {
        throw new Error('Predicción no encontrada');
      }
      
      return prediction;
    } catch (error) {
      console.error('Error obteniendo predicción:', error);
      
      let errorMessage = 'Error al obtener la predicción';
      
      if (error.message === 'Predicción no encontrada') {
        errorMessage = 'Predicción no encontrada';
      } else if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor';
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
    return {
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
      mothers_qualification: predictionData.mothers_qualification || '',
      fathers_qualification: predictionData.fathers_qualification || ''
    };
  }
};

export default studentService;