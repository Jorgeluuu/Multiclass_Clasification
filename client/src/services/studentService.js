import axios from 'axios';

// URL base de la API (puedes configurarla con variables de entorno)
const API_URL = import.meta.env.REACT_APP_API_URL || 'http://localhost:8000';
// Servicio para predicciones académicas
const studentService = {
  /**
Realiza una predicción basada en los datos del estudiante
   * @param {Object} studentData - Datos del estudiante para la predicción
   * @returns {Promise} - Promesa que resuelve con el resultado de la predicción
   */
  predictOutcome: async (studentData) => {
    try {
      const response = await axios.post(`${API_URL}/predict`, studentData);
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
  }
};

export default studentService;