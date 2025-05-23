import React from 'react';
import studentMentoringImage from '../assets/images/student-monitoring.jpg';
import PredictionsList from '../components/PredictionList';

const Monitoring = () => {
  return (
    <div className="w-full">
      {/* Encabezado con imagen de fondo */}
      <div className="relative w-screen left-1/2 right-1/2 -ml-[50vw] -mr-[50vw]">
        <div className="w-full overflow-hidden h-96">
          <img
            src={studentMentoringImage}
            alt="Estudiantes"
            className="object-cover w-full h-full"
          />
          <div className="absolute inset-0 top-0 left-0 w-full h-full bg-black bg-opacity-40"></div>
        </div>
        
        {/* Contenido del encabezado */}
        <div className="absolute top-0 left-0 flex items-center w-full h-full">
          <div className="w-full px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
            <div className="flex flex-col items-start">
              <div className="flex items-center">
                <div className="flex-shrink-0 w-2 h-12 mr-4 bg-red-600"></div>
                <h1 className="text-5xl font-bold text-white font-madrid">
                  Seguimiento
                </h1>
              </div>
              <p className="self-start mt-4 text-xl text-left text-white font-madrid" style={{marginLeft: '0px'}}>
                Panel de control para monitorizar el progreso y rendimiento académico de los estudiantes
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Sección del contenido principal - igual que el form */}
      <div className="px-4 py-12 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="w-full">
          {/* Encabezado rojo igual que el formulario */}
          <div className="p-8 bg-red-600">
            <h2 className="text-3xl font-bold text-center text-white font-madrid">Historial de Predicciones Académicas</h2>
            <p className="mt-2 font-bold text-center text-white font-madrid">Revise y edite las predicciones realizadas anteriormente</p>
          </div>
          
          {/* Contenedor del listado - pegado al encabezado rojo */}
          <div className="border border-gray-200 bg-gray-50">
            <PredictionsList />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Monitoring;