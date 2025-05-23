import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import studentsPredictionImage from '../assets/images/studens-prediction.jpg';
import Button from '../components/Button';
import StudentPredictionForm from '../components/StudentPredictionForm'; 
import studentService from '../services/studentService';

const Prediction = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [predictionResult, setPredictionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Obtener datos iniciales del state de navegación (cuando vienen de Monitoring)
  const initialData = location.state?.initialData || null;
  
  // Limpiar el state de navegación después de usar los datos iniciales
  useEffect(() => {
    if (initialData) {
      console.log('Datos iniciales recibidos desde Monitoring:', initialData);
      // Limpiar el state para evitar que persista en navegaciones futuras
      navigate(location.pathname, { replace: true, state: {} });
    }
  }, [initialData, navigate, location.pathname]);
  
  // Función para manejar el envío del formulario
  const handleFormSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    setPredictionResult(null); // Limpiar resultado anterior
    
    console.log('Enviando datos al backend:', formData);
    
    try {
      const result = await studentService.predictOutcome(formData);
      console.log('Resultado recibido del backend:', result);
      
      setPredictionResult(result);
      
      // Desplazamiento suave hacia los resultados
      setTimeout(() => {
        const resultsSection = document.getElementById('results-section');
        if (resultsSection) {
          resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
      
    } catch (err) {
      console.error('Error al realizar predicción:', err);
      setError(err.message);
      
      // Scroll al área de error
      setTimeout(() => {
        const errorSection = document.getElementById('error-section');
        if (errorSection) {
          errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    } finally {
      setIsLoading(false);
    }
  };

  // Función para limpiar resultados y empezar de nuevo
  const handleNewPrediction = () => {
    setPredictionResult(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Función para ir al historial
  const handleViewHistory = () => {
    navigate('/monitoring');
  };

  return (
    <div className="w-full">
      {/* Encabezado */}
      <div className="relative w-screen left-1/2 right-1/2 -ml-[50vw] -mr-[50vw]">
        <div className="w-full overflow-hidden h-96">
          <img
            src={studentsPredictionImage}
            alt="Estudiantes"
            className="object-cover w-full h-full"
          />
          <div className="absolute inset-0 top-0 left-0 w-full h-full bg-black bg-opacity-40"></div>
        </div>
        
        {/* Contenido encabezado*/}
        <div className="absolute top-0 left-0 flex items-center w-full h-full">
          <div className="w-full px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
            <div className="flex flex-col items-start">
              <div className="flex items-center">
                <div className="flex-shrink-0 w-2 h-12 mr-4 bg-red-600"></div>
                <h1 className="text-5xl font-bold text-white font-madrid">
                  Predicción
                </h1>
              </div>
              <p className="self-start mt-4 text-xl text-left text-white font-madrid" style={{marginLeft: '0px'}}>
                Herramienta para la predicción del rendimiento académico de estudiantes basada en algoritmos de aprendizaje automático
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Sección del formulario */}
      <div className="px-4 py-12 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="w-full">
          
          {/* Indicador de edición (cuando vienen datos) */}
          {initialData && (
            <div className="p-4 mb-6 border border-blue-200 bg-blue-50">
              <div className="flex items-center">
                <div className="flex-shrink-0 w-1 h-6 mr-3 bg-blue-600"></div>
                <div>
                  <h3 className="text-lg font-semibold text-blue-800 font-madrid">Editando predicción existente</h3>
                  <p className="mt-1 text-blue-700 font-madrid">
                    Los campos han sido pre-cargados con los datos de la predicción seleccionada. 
                    Modifique los valores que desee y genere una nueva predicción.
                  </p>
                </div>
              </div>
            </div>
          )}
          
          {/* Contenedor del formulario */}
          <div className="w-full">
            <StudentPredictionForm 
              onSubmit={handleFormSubmit} 
              isLoading={isLoading}
              initialData={initialData}
            />
          </div>
          
          {/* Sección de error */}
          {error && (
            <div id="error-section" className="p-6 mt-8 border border-red-200 bg-red-50">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-red-800 font-madrid">Error al realizar la predicción</h3>
                  <p className="mt-1 text-red-700 font-madrid">{error}</p>
                  <div className="mt-4">
                    <Button
                      variant="secondary"
                      onClick={() => setError(null)}
                      className="px-4 py-2 text-sm"
                    >
                      Cerrar
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {/* Sección de resultados */}
          {predictionResult && (
            <div id="results-section" className="p-6 mt-12 bg-white border border-gray-200">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-gray-800 font-madrid">Resultado de la Predicción</h2>
              </div>
              
              {/* Predicción principal */}
              <div className="p-6 mb-6 text-center border border-gray-200 bg-gray-50">
                <p className="mb-2 text-sm text-gray-500 font-madrid">Resultado más probable:</p>
                <div className="flex items-center justify-center">
                  <span className={`inline-flex px-6 py-3 text-2xl font-bold border font-madrid ${
                    predictionResult.prediction === 'Graduate' ? 'bg-green-100 text-green-800 border-green-200' :
                    predictionResult.prediction === 'Dropout' ? 'bg-red-100 text-red-800 border-red-200' :
                    predictionResult.prediction === 'Enrolled' ? 'bg-blue-100 text-blue-800 border-blue-200' :
                    'bg-gray-100 text-gray-800 border-gray-200'
                  }`}>
                    {predictionResult.prediction === 'Graduate' ? 'Graduado' :
                     predictionResult.prediction === 'Dropout' ? 'Abandono' :
                     predictionResult.prediction === 'Enrolled' ? 'Matriculado' :
                     predictionResult.prediction}
                  </span>
                </div>
              </div>
              
              {/* Barra de probabilidades */}
              {predictionResult.probabilities && (
                <div className="mt-6">
                  <h3 className="mb-4 text-lg font-semibold text-gray-700 font-madrid">Probabilidades por categoría:</h3>
                  <div className="space-y-4">
                    {Object.entries(predictionResult.probabilities).map(([label, prob]) => {
                      const translatedLabel = 
                        label === 'Graduate' ? 'Graduado' :
                        label === 'Dropout' ? 'Abandono' :
                        label === 'Enrolled' ? 'Matriculado' :
                        label;
                      
                      const percentage = (prob * 100).toFixed(1);
                      
                      return (
                        <div key={label}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-sm font-medium text-gray-700 font-madrid">{translatedLabel}</span>
                            <span className="text-sm font-medium text-gray-700 font-madrid">{percentage}%</span>
                          </div>
                          <div className="w-full h-3 overflow-hidden bg-gray-200 rounded-full">
                            <div 
                              className={`h-3 rounded-full transition-all duration-1000 ease-out ${
                                label === 'Dropout' ? 'bg-red-500' : 
                                label === 'Graduate' ? 'bg-green-500' : 'bg-blue-500'
                              }`}
                              style={{ width: `${percentage}%` }}
                            ></div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
              
              {/* Botones de acción */}
              <div className="flex flex-col items-center justify-center mt-8 space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
                <Button 
                  onClick={handleNewPrediction}
                  className="w-full sm:w-auto"
                >
                  Nueva predicción
                </Button>
                <Button 
                  variant="secondary"
                  onClick={handleViewHistory}
                  className="w-full sm:w-auto"
                >
                  Ver todas las predicciones
                </Button>
              </div>

            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Prediction;