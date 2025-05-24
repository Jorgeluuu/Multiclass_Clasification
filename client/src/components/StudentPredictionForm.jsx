import React, { useState, useEffect } from 'react';
import Button from '../components/Button';

const StudentPredictionForm = ({ onSubmit, isLoading, initialData, isEditMode = false }) => {
  const [formData, setFormData] = useState({
    age_at_enrollment: '',
    marital_status: '',
    curricular_units_1st_sem_grade: '',
    curricular_units_1st_sem_approved: '',
    curricular_units_1st_sem_evaluations: '',
    curricular_units_2nd_sem_grade: '',
    curricular_units_2nd_sem_approved: '',
    curricular_units_2nd_sem_evaluations: '',
    unemployment_rate: '',
    gdp: '',
    scholarship_holder: '',
    tuition_fees_up_to_date: '',
    previous_qualification: '',
    mothers_qualification: '', 
    fathers_qualification: ''  
  });
  
  const [errors, setErrors] = useState({});
  
  // Cargar datos iniciales si existen (para edición)
  useEffect(() => {
    if (initialData) {
      console.log('Cargando datos iniciales:', initialData);
      setFormData(prevData => ({
        ...prevData,
        ...initialData
      }));
    }
  }, [initialData]);
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Limpiar error del campo cuando el usuario empiece a escribir
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: null
      }));
    }
  };
  
  // Validar campos requeridos
  const validateForm = () => {
    const newErrors = {};
    
    // Validar edad
    if (!formData.age_at_enrollment) {
      newErrors.age_at_enrollment = "La edad es requerida";
    } else {
      const age = parseFloat(formData.age_at_enrollment);
      if (age < 17 || age > 60) {
        newErrors.age_at_enrollment = "La edad debe estar entre 17 y 60 años";
      }
    }
    
    // Validar estado civil
    if (!formData.marital_status) {
      newErrors.marital_status = "El estado civil es requerido";
    }
    
    // Validar calificaciones
    if (!formData.curricular_units_1st_sem_grade) {
      newErrors.curricular_units_1st_sem_grade = "La calificación es requerida";
    } else {
      const grade = parseFloat(formData.curricular_units_1st_sem_grade);
      if (grade < 0 || grade > 20) {
        newErrors.curricular_units_1st_sem_grade = "La calificación debe estar entre 0 y 20";
      }
    }
    
    if (!formData.curricular_units_2nd_sem_grade) {
      newErrors.curricular_units_2nd_sem_grade = "La calificación es requerida";
    } else {
      const grade = parseFloat(formData.curricular_units_2nd_sem_grade);
      if (grade < 0 || grade > 20) {
        newErrors.curricular_units_2nd_sem_grade = "La calificación debe estar entre 0 y 20";
      }
    }
    
    // Validar otros campos requeridos
    const requiredFields = [
      'curricular_units_1st_sem_approved',
      'curricular_units_1st_sem_evaluations', 
      'curricular_units_2nd_sem_approved',
      'curricular_units_2nd_sem_evaluations',
      'unemployment_rate',
      'gdp',
      'scholarship_holder',
      'tuition_fees_up_to_date',
      'previous_qualification',
      'mothers_qualification',
      'fathers_qualification'
    ];
    
    requiredFields.forEach(field => {
      if (!formData[field]) {
        newErrors[field] = "Este campo es requerido";
      }
    });
    
    return newErrors;
  };
  
  // Manejar el envío del formulario
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validar el formulario
    const formErrors = validateForm();
    if (Object.keys(formErrors).length > 0) {
      setErrors(formErrors);
      // Scroll al primer error encontrado
      const firstErrorField = Object.keys(formErrors)[0];
      const errorElement = document.querySelector(`[name="${firstErrorField}"]`);
      if (errorElement) {
        errorElement.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
        errorElement.focus();
      }
      return;
    }
    
    // Preparar los datos para enviar
    const submissionData = {
      age_at_enrollment: parseFloat(formData.age_at_enrollment),
      marital_status: formData.marital_status,
      curricular_units_1st_sem_grade: parseFloat(formData.curricular_units_1st_sem_grade),
      curricular_units_1st_sem_approved: parseInt(formData.curricular_units_1st_sem_approved),
      curricular_units_1st_sem_evaluations: parseInt(formData.curricular_units_1st_sem_evaluations),
      curricular_units_2nd_sem_grade: parseFloat(formData.curricular_units_2nd_sem_grade),
      curricular_units_2nd_sem_approved: parseInt(formData.curricular_units_2nd_sem_approved),
      curricular_units_2nd_sem_evaluations: parseInt(formData.curricular_units_2nd_sem_evaluations),
      unemployment_rate: parseFloat(formData.unemployment_rate),
      gdp: parseFloat(formData.gdp),
      scholarship_holder: formData.scholarship_holder,
      tuition_fees_up_to_date: formData.tuition_fees_up_to_date,
      previous_qualification: formData.previous_qualification,
      mothers_qualification: formData.mothers_qualification,
      fathers_qualification: formData.fathers_qualification
    };
  
    console.log('Datos enviados:', submissionData);
    onSubmit(submissionData);
  };

  const inputBaseClasses = "w-full p-3 border border-gray-300 bg-white text-gray-800 font-madrid focus:outline-none focus:ring-2 focus:ring-red-600 focus:border-red-600 transition-all duration-200 hover:border-gray-400";
  const labelClasses = "block mb-2 text-sm font-semibold text-gray-800 font-madrid text-left";
  const sectionTitleClasses = "mb-6 text-xl font-bold text-gray-800 font-madrid flex items-center justify-start text-left w-full";
  const sectionClasses = "p-6 bg-gray-50 border border-gray-200 text-left";
  const errorClasses = "mt-1 text-sm text-red-600 font-madrid text-left";
  
  return (
    <div className="w-full font-madrid">
      <div className="p-8 bg-red-600">
        <h2 className="text-3xl font-bold text-left text-white font-madrid md:text-center">
          {isEditMode ? 'Editar Predicción Académica' : 'Formulario de Predicción Académica'}
        </h2>
        <p className="mt-2 font-bold text-left text-white font-madrid md:text-center">
          {isEditMode ? 'Modifique los datos para actualizar la predicción' : 'Complete la información para generar una predicción personalizada'}
        </p>
      </div>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Sección 1: Información Personal */}
        <div className={sectionClasses}>
        <h3 className={sectionTitleClasses}>
        <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
            Información Personal
          </h3>
          
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label className={labelClasses}>Edad al inscribirse *</label>
              <input
                type="number"
                name="age_at_enrollment"
                value={formData.age_at_enrollment}
                onChange={handleChange}
                min="17"
                max="60"
                className={`${inputBaseClasses} ${errors.age_at_enrollment ? 'border-red-500' : ''}`}
                placeholder="Ingrese la edad (17-60 años)"
              />
              {errors.age_at_enrollment && (
                <p className={errorClasses}>{errors.age_at_enrollment}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Estado Civil *</label>
              <select
                name="marital_status"
                value={formData.marital_status}
                onChange={handleChange}
                className={`${inputBaseClasses} ${errors.marital_status ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em'
                }}
              >
                <option value="">Seleccione el estado civil</option>
                <option value="Single">Soltero</option>
                <option value="Married">Casado</option>
                <option value="Divorced">Divorciado</option>
                <option value="Widower">Viudo</option>
                <option value="Legally separated">Separado legalmente</option>
              </select>
              {errors.marital_status && (
                <p className={errorClasses}>{errors.marital_status}</p>
              )}
            </div>
          </div>
        </div>
        
        {/* Sección 2: Información Académica - Primer Semestre */}
        <div className={sectionClasses}>
          <h3 className={sectionTitleClasses}>
            <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div> 
            Información Académica - Primer Semestre
          </h3>
          
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div>
              <label className={labelClasses}>Calificación *</label>
              <input
                type="number"
                name="curricular_units_1st_sem_grade"
                value={formData.curricular_units_1st_sem_grade}
                onChange={handleChange}
                min="0"
                max="20"
                step="0.1"
                className={`${inputBaseClasses} ${errors.curricular_units_1st_sem_grade ? 'border-red-500' : ''}`}
                placeholder="Calificación (0.0 - 20.0)"
              />
              {errors.curricular_units_1st_sem_grade && (
                <p className={errorClasses}>{errors.curricular_units_1st_sem_grade}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Unidades aprobadas *</label>
              <input
                type="number"
                name="curricular_units_1st_sem_approved"
                value={formData.curricular_units_1st_sem_approved}
                onChange={handleChange}
                min="0"
                max="10"
                className={`${inputBaseClasses} ${errors.curricular_units_1st_sem_approved ? 'border-red-500' : ''}`}
                placeholder="Número de unidades (0-10)"
              />
              {errors.curricular_units_1st_sem_approved && (
                <p className={errorClasses}>{errors.curricular_units_1st_sem_approved}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Evaluaciones *</label>
              <input
                type="number"
                name="curricular_units_1st_sem_evaluations"
                value={formData.curricular_units_1st_sem_evaluations}
                onChange={handleChange}
                min="0"
                max="15"
                className={`${inputBaseClasses} ${errors.curricular_units_1st_sem_evaluations ? 'border-red-500' : ''}`}
                placeholder="Número de evaluaciones (0-15)"
              />
              {errors.curricular_units_1st_sem_evaluations && (
                <p className={errorClasses}>{errors.curricular_units_1st_sem_evaluations}</p>
              )}
            </div>
          </div>
        </div>
        
        {/* Sección 3: Información Académica - Segundo Semestre */}
        <div className={sectionClasses}>
          <h3 className={sectionTitleClasses}>
            <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
            Información Académica - Segundo Semestre
          </h3>
          
          <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            <div>
              <label className={labelClasses}>Calificación *</label>
              <input
                type="number"
                name="curricular_units_2nd_sem_grade"
                value={formData.curricular_units_2nd_sem_grade}
                onChange={handleChange}
                min="0"
                max="20"
                step="0.1"
                className={`${inputBaseClasses} ${errors.curricular_units_2nd_sem_grade ? 'border-red-500' : ''}`}
                placeholder="Calificación (0.0 - 20.0)"
              />
              {errors.curricular_units_2nd_sem_grade && (
                <p className={errorClasses}>{errors.curricular_units_2nd_sem_grade}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Unidades aprobadas *</label>
              <input
                type="number"
                name="curricular_units_2nd_sem_approved"
                value={formData.curricular_units_2nd_sem_approved}
                onChange={handleChange}
                min="0"
                max="10"
                className={`${inputBaseClasses} ${errors.curricular_units_2nd_sem_approved ? 'border-red-500' : ''}`}
                placeholder="Número de unidades (0-10)"
              />
              {errors.curricular_units_2nd_sem_approved && (
                <p className={errorClasses}>{errors.curricular_units_2nd_sem_approved}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Evaluaciones *</label>
              <input
                type="number"
                name="curricular_units_2nd_sem_evaluations"
                value={formData.curricular_units_2nd_sem_evaluations}
                onChange={handleChange}
                min="0"
                max="15"
                className={`${inputBaseClasses} ${errors.curricular_units_2nd_sem_evaluations ? 'border-red-500' : ''}`}
                placeholder="Número de evaluaciones (0-15)"
              />
              {errors.curricular_units_2nd_sem_evaluations && (
                <p className={errorClasses}>{errors.curricular_units_2nd_sem_evaluations}</p>
              )}
            </div>
          </div>
        </div>
        
        {/* Sección 4: Información Económica */}
        <div className={sectionClasses}>
          <h3 className={sectionTitleClasses}>
            <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
            Información Económica
          </h3>
          
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
            <div>
              <label className={labelClasses}>Tasa de desempleo (%) *</label>
              <input
                type="number"
                name="unemployment_rate"
                value={formData.unemployment_rate}
                onChange={handleChange}
                min="7"
                max="20"
                step="0.1"
                className={`${inputBaseClasses} ${errors.unemployment_rate ? 'border-red-500' : ''}`}
                placeholder="Porcentaje de desempleo (7.0 - 20.0)"
              />
              {errors.unemployment_rate && (
                <p className={errorClasses}>{errors.unemployment_rate}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>PIB (% crecimiento) *</label>
              <input
                type="number"
                name="gdp"
                value={formData.gdp}
                onChange={handleChange}
                min="-5"
                max="5"
                step="0.1"
                className={`${inputBaseClasses} ${errors.gdp ? 'border-red-500' : ''}`}
                placeholder="Crecimiento del PIB (-5.0 - 5.0)"
              />
              {errors.gdp && (
                <p className={errorClasses}>{errors.gdp}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Becario *</label>
              <select
                name="scholarship_holder"
                value={formData.scholarship_holder}
                onChange={handleChange}
                className={`${inputBaseClasses} ${errors.scholarship_holder ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em'
                }}
              >
                <option value="">¿Tiene beca?</option>
                <option value="Yes">Sí</option>
                <option value="No">No</option>
              </select>
              {errors.scholarship_holder && (
                <p className={errorClasses}>{errors.scholarship_holder}</p>
              )}
            </div>
            
            <div>
              <label className={labelClasses}>Tasas de matrícula al día *</label>
              <select
                name="tuition_fees_up_to_date"
                value={formData.tuition_fees_up_to_date}
                onChange={handleChange}
                className={`${inputBaseClasses} ${errors.tuition_fees_up_to_date ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em'
                }}
              >
                <option value="">¿Pagos al día?</option>
                <option value="Yes">Sí</option>
                <option value="No">No</option>
              </select>
              {errors.tuition_fees_up_to_date && (
                <p className={errorClasses}>{errors.tuition_fees_up_to_date}</p>
              )}
            </div>
          </div>
        </div>
        
        {/* Sección 5: Información del Antecedente Educativo */}
        <div className={sectionClasses}>
          <h3 className={sectionTitleClasses}>
            <div className="flex-shrink-0 w-1 h-6 mr-3 bg-red-600"></div>
            Antecedentes Educativos
          </h3>
          
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label className={labelClasses}>Calificación previa del estudiante *</label>
              <select
                name="previous_qualification"
                value={formData.previous_qualification}
                onChange={handleChange}
                className={`${inputBaseClasses} ${errors.previous_qualification ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                style={{
                  backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                  backgroundPosition: 'right 0.75rem center',
                  backgroundRepeat: 'no-repeat',
                  backgroundSize: '1.5em 1.5em'
                }}
              >
                <option value="">Seleccione la calificación previa</option>
                <option value="Secondary education">Educación secundaria</option>
                <option value="Higher education—bachelor's degree">Grado universitario</option>
                <option value="Higher education—degree">Licenciatura</option>
                <option value="Higher education—master's degree">Máster</option>
                <option value="Higher education—doctorate">Doctorado</option>
                <option value="Frequency of higher education">Frecuencia de educación superior</option>
                <option value="Professional higher technical course">Curso técnico superior profesional</option>
                <option value="Technological specialization course">Curso de especialización tecnológica</option>
                <option value="Basic education 3rd cycle (9th/10th/11th year) or equivalent">Educación básica 3er ciclo</option>
                <option value="Basic education 2nd cycle (6th/7th/8th year) or equivalent">Educación básica 2º ciclo</option>
                <option value="12th year of schooling—not completed">12º año no completado</option>
                <option value="11th year of schooling—not completed">11º año no completado</option>
                <option value="10th year of schooling—not completed">10º año no completado</option>
                <option value="Other—11th year of schooling">Otro - 11º año</option>
              </select>
              {errors.previous_qualification && (
                <p className={errorClasses}>{errors.previous_qualification}</p>
              )}
            </div>
            
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
              <div>
                <label className={labelClasses}>Calificación de la madre *</label>
                <select
                  name="mothers_qualification"
                  value={formData.mothers_qualification}
                  onChange={handleChange}
                  className={`${inputBaseClasses} ${errors.mothers_qualification ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                  style={{
                    backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                    backgroundPosition: 'right 0.75rem center',
                    backgroundRepeat: 'no-repeat',
                    backgroundSize: '1.5em 1.5em'
                  }}
                >
                  <option value="">Seleccione nivel educativo</option>
                  <option value="Secondary education—12th year of schooling or equivalent">Educación secundaria</option>
                  <option value="Higher education—bachelor's degree">Grado universitario</option>
                  <option value="Higher education—degree">Licenciatura</option>
                  <option value="Higher education—master's degree">Máster</option>
                  <option value="Higher education—doctorate">Doctorado</option>
                  <option value="Basic education 3rd cycle (9th/10th/11th year) or equivalent">Educación básica 3er ciclo</option>
                  <option value="Basic education 2nd cycle (6th/7th/8th year) or equivalent">Educación básica 2º ciclo</option>
                  <option value="Basic education 1st cycle (4th/5th year) or equivalent">Educación básica 1er ciclo</option>
                  <option value="Can read without having a 4th year of schooling">Puede leer sin tener 4º año</option>
                  <option value="Cannot read or write">No sabe leer ni escribir</option>
                  <option value="Unknown">Desconocido</option>
                  <option value="7th year of schooling">7º año de escolaridad</option>
                  <option value="Other—11th year of schooling">Otro - 11º año</option>
                  <option value="2nd cycle of the general high school course">2º ciclo del curso general de bachillerato</option>
                  <option value="Technological specialization course">Curso de especialización tecnológica</option>
                </select>
                {errors.mothers_qualification && (
                  <p className={errorClasses}>{errors.mothers_qualification}</p>
                )}
              </div>
              
              <div>
                <label className={labelClasses}>Calificación del padre *</label>
                <select
                  name="fathers_qualification"
                  value={formData.fathers_qualification}
                  onChange={handleChange}
                  className={`${inputBaseClasses} ${errors.fathers_qualification ? 'border-red-500' : ''} appearance-none bg-white cursor-pointer`}
                  style={{
                    backgroundImage: `url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e")`,
                    backgroundPosition: 'right 0.75rem center',
                    backgroundRepeat: 'no-repeat',
                    backgroundSize: '1.5em 1.5em'
                  }}
                >
                  <option value="">Seleccione nivel educativo</option>
                  <option value="Secondary education—12th year of schooling or equivalent">Educación secundaria</option>
                  <option value="Higher education—bachelor's degree">Grado universitario</option>
                  <option value="Higher education—degree">Licenciatura</option>
                  <option value="Higher education—master's degree">Máster</option>
                  <option value="Higher education—doctorate">Doctorado</option>
                  <option value="Basic education 3rd cycle (9th/10th/11th year) or equivalent">Educación básica 3er ciclo</option>
                  <option value="Basic education 2nd cycle (6th/7th/8th year) or equivalent">Educación básica 2º ciclo</option>
                  <option value="Basic education 1st cycle (4th/5th year) or equivalent">Educación básica 1er ciclo</option>
                  <option value="Can read without having a 4th year of schooling">Puede leer sin tener 4º año</option>
                  <option value="Cannot read or write">No sabe leer ni escribir</option>
                  <option value="Unknown">Desconocido</option>
                  <option value="7th year of schooling">7º año de escolaridad</option>
                  <option value="Other—11th year of schooling">Otro - 11º año</option>
                  <option value="2nd cycle of the general high school course">2º ciclo del curso general de bachillerato</option>
                  <option value="Technological specialization course">Curso de especialización tecnológica</option>
                </select>
                {errors.fathers_qualification && (
                  <p className={errorClasses}>{errors.fathers_qualification}</p>
                )}
              </div>
            </div>
          </div>
        </div>
        
        {/* Botón de envío */}
        <div className="flex justify-center p-8 border border-gray-200 bg-gray-50">
        <Button
            type="submit"
            variant="primary"
            className="px-8 py-4 text-lg disabled:bg-red-300 disabled:cursor-not-allowed"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center">
                <svg className="w-5 h-5 mr-3 animate-spin" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"/>
                </svg>
                Procesando...
              </span>
            ) : (
              isEditMode ? 'Actualizar Predicción' : 'Generar Predicción'
            )}
          </Button>
        </div>
      </form>
    </div>
  );
};

export default StudentPredictionForm;