import axios from 'axios';

// URL base de la API (puedes configurarla con variables de entorno)
const API_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000';

// Servicio para predicciones académicas
const studentService = {
  /**
   * Reordena los datos del formulario al orden exacto del pipeline de ML
   * @param {Object} formData - Datos del formulario
   * @returns {Object} - Datos reordenados según el pipeline
   */
  reorderForPipeline: (formData) => {
    return {
      // Orden exacto del pipeline (1-15)
      curricular_units_1st_sem_grade: parseFloat(formData.curricular_units_1st_sem_grade),
      curricular_units_2nd_sem_grade: parseFloat(formData.curricular_units_2nd_sem_grade),
      curricular_units_1st_sem_approved: parseFloat(formData.curricular_units_1st_sem_approved),
      curricular_units_2nd_sem_approved: parseFloat(formData.curricular_units_2nd_sem_approved),
      curricular_units_1st_sem_evaluations: parseFloat(formData.curricular_units_1st_sem_evaluations),
      curricular_units_2nd_sem_evaluations: parseFloat(formData.curricular_units_2nd_sem_evaluations),
      unemployment_rate: parseFloat(formData.unemployment_rate),
      gdp: parseFloat(formData.gdp),
      age_at_enrollment: parseFloat(formData.age_at_enrollment),
      scholarship_holder: formData.scholarship_holder,
      tuition_fees_up_to_date: formData.tuition_fees_up_to_date,
      marital_status: formData.marital_status,
      previous_qualification: formData.previous_qualification,
      "mother's_qualification": formData["mother's_qualification"],
      "father's_qualification": formData["father's_qualification"]
    };
  },

  /**
   * Realiza una predicción basada en los datos del estudiante
   * @param {Object} studentData - Datos del estudiante para la predicción
   * @returns {Promise} - Promesa que resuelve con el resultado de la predicción
   */
  predictOutcome: async (studentData) => {
    try {
      // Reordenar datos según el pipeline antes de enviar
      const reorderedData = studentService.reorderForPipeline(studentData);
      
      const response = await axios.post(`${API_URL}/predict`, reorderedData);
      return response.data;
    } catch (error) {
      // Manejo de errores centralizado
      console.error('Error realizando la predicción:', error);
      
      // Devolver un objeto de error estructurado
      let errorMessage = 'Error al realizar la predicción';
      
      if (error.response) {
        // El servidor respondió con un código de estado fuera del rango 2xx
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        // La petición se realizó pero no se recibió respuesta
        errorMessage = 'No se recibió respuesta del servidor';
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Obtiene todas las predicciones realizadas
   * @param {Object} params - Parámetros de consulta (limit, offset, filter)
   * @returns {Promise} - Promesa que resuelve con el listado de predicciones
   */
  getAllPredictions: async (params = {}) => {
    try {
      const { limit = 100, offset = 0, outcome_filter = null } = params;
      
      const queryParams = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      });
      
      if (outcome_filter) {
        queryParams.append('outcome_filter', outcome_filter);
      }
      
      const response = await axios.get(`${API_URL}/predictions?${queryParams}`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo predicciones:', error);
      
      let errorMessage = 'Error al obtener el listado de predicciones';
      
      if (error.response) {
        errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor';
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
      const response = await axios.get(`${API_URL}/predictions/${predictionId}`);
      return response.data;
    } catch (error) {
      console.error('Error obteniendo predicción:', error);
      
      let errorMessage = 'Error al obtener la predicción';
      
      if (error.response) {
        if (error.response.status === 404) {
          errorMessage = 'Predicción no encontrada';
        } else {
          errorMessage = error.response.data.detail || error.response.data.message || `Error ${error.response.status}`;
        }
      } else if (error.request) {
        errorMessage = 'No se recibió respuesta del servidor';
      }
      
      throw new Error(errorMessage);
    }
  },

  /**
   * Convierte los datos de la base de datos al formato del formulario
   * Útil para cargar datos existentes en el formulario de edición
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
      "mother's_qualification": predictionData.mothers_qualification || '', // Nota: sin apóstrofe en BD
      "father's_qualification": predictionData.fathers_qualification || ''   // Nota: sin apóstrofe en BD
    };
  }
};

export default studentService;