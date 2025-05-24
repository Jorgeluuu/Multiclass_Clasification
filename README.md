# Sistema de Clasificación Multiclase para Predicción de Éxito Académico

## 📚 Descripción del Proyecto

Este proyecto implementa un sistema de clasificación multiclase para predecir el éxito académico de estudiantes universitarios. El sistema puede clasificar a los estudiantes en tres categorías:
- Dropout (Abandono)
- Graduate (Graduado)
- Enrolled (Matriculado)

Utiliza técnicas avanzadas de aprendizaje automático, específicamente XGBoost y Random Forest, para realizar predicciones basadas en diversos factores académicos y socioeconómicos.

## 🏗️ Estructura del Proyecto

```
Multiclass_Clasification/
│
├── 📁 data/                                    # Datos del proyecto
│   ├── raw/
│   │   └── raw_data.csv                        # Datos originales sin procesar
│   └── processed/
│       └── dataset_procesado.csv               # Datos limpios y transformados para ML
│
├── 📁 notebooks/                               # Análisis exploratorio y experimentación
│   ├── EDA.ipynb                              # Análisis Exploratorio de Datos completo
│   └── data_cleaning.ipynb                    # Limpieza y preprocesamiento de datos
│
├── 📁 model_training/                          # Entrenamiento de modelos ML
│   ├── xgboost.ipynb                          # Entrenamiento del modelo XGBoost
│   └── random_forest.ipynb                    # Entrenamiento del modelo Random Forest
│
├── 📁 models/                                  # Modelos entrenados y artefactos
│   ├── xgboost.ipynb                          # Notebook de entrenamiento XGBoost
│   └── trained/
│       ├── xgboost_multiclass_model.pkl       # Modelo XGBoost serializado
│       └── ...                                # Otros modelos entrenados
│
├── 📁 server/                                  # Backend de la aplicación (Python/FastAPI)
│   ├── __init__.py                            # Hace que server sea un paquete Python
│   ├── main.py                                # Punto de entrada del servidor FastAPI
│   ├── __pycache__/                           # Archivos compilados de Python
│   │
│   ├── 📁 models/                             # Lógica de Machine Learning
│   │   ├── preprocessing.py                   # Pipeline de preprocesamiento de datos
│   │   ├── predictor.py                       # Función principal de predicción
│   │   └── schemas.py                         # Esquemas de validación con Pydantic
│   │
│   ├── 📁 database/                           # Gestión de base de datos
│   │   ├── migrations.py                      # Sistema de migración y creación de tablas
│   │   └── supabase_client.py                 # Cliente para conectar con Supabase
│   │
│   ├── 📁 artifacts/                          # Modelos y pipelines serializados
│   │   ├── xgboost_multiclass_pipeline.pkl    # Pipeline de preprocesamiento serializado
│   │   ├── xgboost_multiclass_model.pkl       # Modelo XGBoost para producción
│   │   └── ...                                # Otros artefactos ML
│   │
│   └── 📁 tests/                              # Tests unitarios y de integración
│       ├── test_preprocessing.py              # Tests del pipeline de preprocesamiento
│       ├── test_predictor.py                  # Tests de la función de predicción
│       └── test_migrations.py                 # Tests del sistema de migración
│
├── 📁 client/                                  # Frontend de la aplicación (React/Vite)
│   ├── index.html                             # Archivo HTML principal
│   ├── package.json                           # Dependencias y scripts de npm
│   ├── eslint.config.js                       # Configuración del linter
│   ├── postcss.config.js                      # Configuración de PostCSS
│   ├── tailwind.config.js                     # Configuración de Tailwind CSS
│   │
│   └── 📁 src/                                # Código fuente del frontend
│       ├── main.jsx                           # Punto de entrada de la aplicación React
│       ├── App.jsx                            # Componente principal de la aplicación
│       │
│       ├── 📁 components/                     # Componentes reutilizables de React
│       │   ├── Button.jsx                     # Componente de botón personalizado
│       │   ├── Navbar.jsx                     # Barra de navegación superior
│       │   ├── Footer.jsx                     # Pie de página
│       │   ├── StudentPredictionForm.jsx      # Formulario principal de predicción
│       │   └── PredictionList.jsx             # Lista/tabla de predicciones históricas
│       │
│       ├── 📁 pages/                          # Páginas principales de la aplicación
│       │   ├── Prediction.jsx                 # Página de nueva predicción
│       │   └── Monitoring.jsx                 # Página de seguimiento y historial
│       │
│       ├── 📁 services/                       # Servicios para comunicación con API
│       │   └── studentService.js              # Servicio para llamadas al backend
│       │
│       └── 📁 assets/                         # Recursos estáticos
│           └── images/                        # Imágenes de la aplicación
│               ├── madrid-logo.png            # Logo 
│               ├── student-monitoring.jpg     # Imagen para página de seguimiento
│               └── students-prediction.jpg    # Imagen para página de predicción
│
├── requirements.txt                            # Dependencias de Python del backend
├── README.md                                  # Documentación del proyecto
└── .gitignore                                 # Archivos a ignorar por Git
```

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.13+
- XGBoost
- Scikit-learn
- FastAPI

### Frontend
- React
- Tailwind CSS
- Vite

### Base de Datos
- Supabase

## 📋 Requisitos Previos

- Python 3.13 o superior
- Node.js y npm
- Git

## 🚀 Instalación y Configuración
### Backend

1. Clonar el repositorio:
```bash
git clone [URL del repositorio]
cd Multiclass_Clasification
```

2. Crear y activar entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
source env/Scripts/activate #Windows-Bash
```

3. Instalar dependencias desde requirements.txt:
```bash
pip install -r requirements.txt
```

4. Levantar el backend
(raiz del proyecto): 
```bash
uvicorn server.main:app --reload
```

### Preparación de Datos

1. Crear las carpetas necesarias para los datos:
```bash
mkdir -p data/raw data/processed
```

2. Colocar el archivo CSV con los datos del estudiante en la carpeta correspondiente:
- Datos sin procesar: `data/raw/student_data.csv`
   Debes descargar el dataset de [Predict students' dropout and academic success](https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset) y colocarlo en la carpeta `data/raw/`.

- Datos procesados: `data/processed/processed_data.csv`
   Estos se crearan automaticamente

### Frontend

1. Navegar al directorio del cliente:
```bash
cd client
```

2. Instalar dependencias:
```bash
npm install
npm run dev
```

## 🎯 Características Principales

- Predicción multiclase del éxito académico
- Interfaz web interactiva
- API RESTful para predicciones
- Preprocesamiento automático de datos
- Modelos de machine learning optimizados

## 📊 Modelos de Machine Learning

El proyecto implementa dos modelos principales:

1. **XGBoost (Modelo Principal)**
   - Precisión en conjunto de prueba: ~85%
   - Optimizado para manejo de clases desbalanceadas
   - Hiperparámetros ajustados mediante Optuna

2. **Random Forest (Modelo Alternativo)**
   - Implementado como modelo de respaldo
   - Buena interpretabilidad de características

## 🔄 Flujo de Trabajo

1. Los datos del estudiante se ingresan a través de la interfaz web
2. El backend procesa y preprocesa los datos
3. El modelo realiza la predicción
4. Los resultados se muestran en la interfaz de usuario

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor, sigue estos pasos:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.
