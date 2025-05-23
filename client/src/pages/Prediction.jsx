import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import studentsPredictionImage from '../assets/images/studens-prediction.jpg';
import Button from '../components/Button';
import StudentPredictionForm from '../components/StudentPredictionForm'; 
import studentService from '../services/studentService';

const Prediction = () => {
  const location = useLocation();
  const [predictionResult, setPredictionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  
  // Obtener datos iniciales del state de navegación (cuando vienen de Monitoring)
  const initialData = location.state?.initialData || null;
  
  // Función para manejar el envío del formulario
  const handleFormSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await studentService.predictOutcome(formData);
      setPredictionResult(result);
      // Desplazamiento suave hacia los resultados
      if (result) {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
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
                <h1 className="text-5xl font-bold text-white">
                  Predicción
                </h1>
              </div>
              <p className="self-start mt-4 text-xl text-left text-white" style={{marginLeft: '0px'}}>
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
            <div className="p-4 mt-8 text-red-700 bg-red-100 border border-red-400">
              <p className="font-bold font-madrid">Error:</p>
              <p className="font-madrid">{error}</p>
            </div>
          )}
          
          {/* Sección de resultados */}
          {predictionResult && (
            <div id="results-section" className="p-6 mt-12 bg-white border border-gray-200">
              <h2 className="mb-6 text-2xl font-bold text-gray-800 font-madrid">Resultado de la Predicción</h2>
              
              {/* Predicción principal */}
              <div className="p-4 mb-6 text-center border border-gray-200 bg-gray-50">
                <p className="mb-2 text-sm text-gray-500 font-madrid">Resultado más probable:</p>
                <p className="text-2xl font-bold text-gray-800 font-madrid">{predictionResult.prediction}</p>
              </div>
              
              {/* Barra de probabilidades */}
              <div className="mt-6">
                <h3 className="mb-4 text-lg font-semibold text-gray-700 font-madrid">Probabilidades por categoría:</h3>
                <div className="space-y-4">
                  {Object.entries(predictionResult.probabilities).map(([label, prob]) => (
                    <div key={label}>
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700 font-madrid">{label}</span>
                        <span className="text-sm font-medium text-gray-700 font-madrid">{(prob * 100).toFixed(1)}%</span>
                      </div>
                      <div className="w-full h-2.5 bg-gray-200">
                        <div 
                          className={`h-2.5 ${
                            label === 'Dropout' ? 'bg-orange-500' : 
                            label === 'Graduate' ? 'bg-green-500' : 'bg-blue-500'
                          }`}
                          style={{ width: `${prob * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              
              {/* Botón para hacer nueva predicción */}
              <div className="mt-8 text-center">
                <Button 
                  onClick={() => {
                    setPredictionResult(null); 
                    window.scrollTo({ top: 0, behavior: 'smooth' });
                  }}
                >
                  Nueva predicción
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