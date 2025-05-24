import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Button from './Button';
import studentService from '../services/studentService';

const PredictionsList = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [outcomeFilter, setOutcomeFilter] = useState('');
  
  const navigate = useNavigate();
  const itemsPerPage = 10;

  // Cargar predicciones
  const loadPredictions = async (page = 1, filter = '') => {
    setLoading(true);
    setError(null);
    
    try {
      const offset = (page - 1) * itemsPerPage;
      const params = {
        limit: itemsPerPage,
        offset,
        ...(filter && { outcome_filter: filter })
      };
      
      console.log('Cargando predicciones con parámetros:', params);
      const response = await studentService.getAllPredictions(params);
      console.log('Respuesta del servicio:', response);
      
      // El servicio ya maneja la estructura correcta
      setPredictions(response.data || []);
      setTotalPages(response.totalPages || Math.ceil((response.total || 0) / itemsPerPage));
      
    } catch (err) {
      console.error('Error cargando predicciones:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Effect para cargar datos iniciales
  useEffect(() => {
    loadPredictions(currentPage, outcomeFilter);
  }, [currentPage, outcomeFilter]);

  // Manejar filtro por outcome
  const handleFilterChange = (filter) => {
    setOutcomeFilter(filter);
    setCurrentPage(1); // Reset a la primera página
  };

  // Manejar actualización manual
  const handleRefresh = () => {
    loadPredictions(currentPage, outcomeFilter);
  };

  // Manejar edición de predicción
  const handleEdit = (prediction) => {
    console.log('Editando predicción:', prediction);
    
    // Convertir datos de BD a formato del formulario
    const formData = studentService.convertToFormFormat(prediction);
    console.log('Datos convertidos para formulario:', formData);
    
    // ✅ SOLO AÑADIR predictionId al state
    navigate('/', { 
      state: { 
        initialData: formData,
        predictionId: prediction.id  // ✅ Pasar el ID
      } 
    });
  };

  // Formatear fecha
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    
    try {
      return new Date(dateString).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (_) {
      return 'Fecha inválida';
    }
  };

  // Formatear probabilidad como porcentaje
  const formatProbability = (probability) => {
    if (probability === null || probability === undefined) return 'N/A';
    return `${(probability * 100).toFixed(1)}%`;
  };

  // Obtener color del badge según el outcome
  const getOutcomeBadgeClass = (outcome) => {
    if (!outcome) return 'bg-gray-100 text-gray-800 border-gray-200';
    
    switch (outcome.toLowerCase()) {
      case 'graduate':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'dropout':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'enrolled':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  // Traducir outcome al español
  const translateOutcome = (outcome) => {
    if (!outcome) return 'N/A';
    
    switch (outcome.toLowerCase()) {
      case 'graduate':
        return 'Graduado';
      case 'dropout':
        return 'Abandono';
      case 'enrolled':
        return 'Matriculado';
      default:
        return outcome;
    }
  };

  // Traducir estado civil
  const translateMaritalStatus = (status) => {
    if (!status) return 'N/A';
    
    switch (status) {
      case 'Single': return 'Soltero';
      case 'Married': return 'Casado';
      case 'Divorced': return 'Divorciado';
      case 'Widower': return 'Viudo';
      case 'Legally separated': return 'Separado';
      default: return status;
    }
  };

  // Obtener la predicción principal de los datos
  const getPredictedOutcome = (prediction) => {
    // Primero intentar con predicted_outcome (que debería venir del backend)
    if (prediction.predicted_outcome) {
      return prediction.predicted_outcome;
    }
    
    // Si no, intentar con target (fallback)
    if (prediction.target) {
      return prediction.target;
    }
    
    // Si tiene probabilidades, determinar la más alta
    if (prediction.probability_graduate || prediction.probability_dropout || prediction.probability_enrolled) {
      const probs = {
        'Graduate': prediction.probability_graduate || 0,
        'Dropout': prediction.probability_dropout || 0,
        'Enrolled': prediction.probability_enrolled || 0
      };
      
      const maxProb = Math.max(...Object.values(probs));
      const predictedClass = Object.keys(probs).find(key => probs[key] === maxProb);
      return predictedClass;
    }
    
    return 'N/A';
  };

  // Obtener la probabilidad principal
  const getMainProbability = (prediction) => {
    const outcome = getPredictedOutcome(prediction);
    
    switch (outcome) {
      case 'Graduate':
        return prediction.probability_graduate;
      case 'Dropout':
        return prediction.probability_dropout;
      case 'Enrolled':
        return prediction.probability_enrolled;
      default:
        return null;
    }
  };

  if (loading) {
    return (
      <div className="p-6 border border-gray-200 bg-gray-50">
        <div className="flex items-center justify-center py-12">
          <div className="flex items-center space-x-3">
            <svg className="w-6 h-6 text-red-600 animate-spin" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
            </svg>
            <span className="text-gray-600 font-madrid">Cargando predicciones...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 border border-gray-200 bg-gray-50">
        <div className="p-6 border border-red-200 bg-red-50">
          <div className="flex items-center">
            <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
            <div>
              <h3 className="text-lg font-semibold text-red-800 font-madrid">Error al cargar predicciones</h3>
              <p className="mt-1 text-red-700 font-madrid">{error}</p>
              <div className="mt-3">
                <Button
                  variant="secondary"
                  onClick={handleRefresh}
                  className="px-4 py-2 text-sm"
                >
                  Reintentar
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="border border-gray-200 bg-gray-50">
      {/* Header con filtros - estilo del formulario */}
      <div className="p-6 border-b border-gray-200 bg-gray-50">
      <h3 className="flex items-center justify-start w-full mb-6 text-xl font-bold text-left text-gray-800 font-madrid">
          <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
          Historial de Predicciones
        </h3>
        
        <div className="flex flex-col space-y-4 lg:flex-row lg:items-center lg:justify-between lg:space-y-0">
          {/* Contador de predicciones  */}
          <div className="flex-shrink-0">
            <p className="text-left text-gray-600 font-madrid lg:text-left">
              {predictions.length} predicciones encontradas
            </p>
          </div>
          
      
          <div className="flex flex-col space-y-3 sm:flex-row sm:items-start lg:items-center sm:space-y-0 sm:space-x-3">
            {/* Filtro por outcome*/}
            <div className="flex flex-col space-y-2 sm:flex-row sm:items-start lg:items-center sm:space-y-0 sm:space-x-3">
              <label className="text-sm font-semibold text-left text-gray-700 font-madrid whitespace-nowrap sm:text-left lg:text-left">
                Filtrar por resultado:
              </label>
              <select
                value={outcomeFilter}
                onChange={(e) => handleFilterChange(e.target.value)}
                className="w-full px-3 py-3 text-gray-800 transition-all duration-200 bg-white border border-gray-300 appearance-none cursor-pointer sm:w-48 lg:w-56 font-madrid focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-red-600"
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em'
                }}
              >
                <option value="">Todos los resultados</option>
                <option value="Graduate">Graduados</option>
                <option value="Dropout">Abandonos</option>
                <option value="Enrolled">Matriculados</option>
              </select>
            </div>
            
            {/* Botón actualizar */}
            <Button
              variant="secondary"
              onClick={handleRefresh}
              className="w-full px-4 py-3 text-sm sm:w-auto whitespace-nowrap"
              disabled={loading}
            >
              Actualizar
            </Button>
          </div>
        </div>
      </div>

      {/* Contenido de la tabla */}
      <div className="p-6">
        {predictions.length === 0 ? (
          <div className="p-8 text-center bg-white border border-gray-200">
            <div className="flex items-center justify-center mb-4">
              <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
              <h3 className="text-lg font-semibold text-gray-800 font-madrid">No hay predicciones</h3>
            </div>
            <p className="mb-6 text-gray-600 font-madrid">
              {outcomeFilter ? `No se encontraron predicciones con resultado "${translateOutcome(outcomeFilter)}"` 
                            : 'Aún no se han realizado predicciones. Comienza creando tu primera predicción.'}
            </p>
            <Button onClick={() => navigate('/')}>
              Crear primera predicción
            </Button>
          </div>
        ) : (
          <div className="overflow-hidden bg-white border border-gray-200">
            <div className="overflow-x-auto">
              <table className="min-w-full bg-white">
                <thead className="bg-gray-50">
                  <tr>
                  <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Nº Expediente
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Fecha
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Edad
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Estado Civil
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Calificaciones
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Resultado
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Probabilidad
                    </th>
                    <th className="px-4 py-3 text-xs font-semibold tracking-wider text-center text-gray-700 uppercase border-b font-madrid">
                      Acciones
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {predictions.map((prediction, index) => {
                    const predictedOutcome = getPredictedOutcome(prediction);
                    const mainProbability = getMainProbability(prediction);
                    
                    return (
                      <tr key={prediction.id || index} className="transition-colors duration-150 hover:bg-gray-50">
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          #{prediction.id || 'N/A'}
                        </td>
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          {formatDate(prediction.created_at)}
                        </td>
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          {prediction.age_at_enrollment ? `${prediction.age_at_enrollment} años` : 'N/A'}
                        </td>
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          {translateMaritalStatus(prediction.marital_status)}
                        </td>
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          <div className="space-y-1">
                            <div>1º Sem: {prediction.curricular_units_1st_sem_grade || 'N/A'}</div>
                            <div>2º Sem: {prediction.curricular_units_2nd_sem_grade || 'N/A'}</div>
                          </div>
                        </td>
                        <td className="px-4 py-4 text-center">
                          <span className={`inline-flex px-3 py-1 text-sm font-medium border font-madrid ${getOutcomeBadgeClass(predictedOutcome)}`}>
                            {translateOutcome(predictedOutcome)}
                          </span>
                        </td>
                        <td className="px-4 py-4 text-sm text-center text-gray-800 font-madrid">
                          {formatProbability(mainProbability)}
                        </td>
                        <td className="px-4 py-4 text-center">
                          <Button
                            variant="secondary"
                            onClick={() => handleEdit(prediction)}
                            className="px-4 py-2 text-sm"
                          >
                            Editar
                          </Button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Paginación */}
        {totalPages > 1 && (
          <div className="flex items-center justify-between mt-6">
            <div className="text-sm text-gray-700 font-madrid">
              Página {currentPage} de {totalPages}
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="secondary"
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="px-3 py-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Anterior
              </Button>
              <Button
                variant="secondary"
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="px-3 py-2 text-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Siguiente
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default PredictionsList;