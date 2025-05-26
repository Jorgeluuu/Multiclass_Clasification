# Sistema de Clasificación Multiclase para Predicción de Éxito Académico

## 📱 Capturas de Pantalla

<div align="center">
  <img src="https://github.com/Jorgeluuu/Multiclass_Clasification/blob/feature/frontend/client/src/assets/images/Macbook-Pro-16-2110x1286.png" alt="Vista Desktop" width="450" style="margin-right: 20px;"/>
  <img src="https://github.com/Jorgeluuu/Multiclass_Clasification/blob/feature/frontend/client/src/assets/images/iPhone-14-Pro-Max-473x968.png" alt="Vista Móvil" width="135"/>
  <br/>
  <em>Interfaz Desktop y Móvil - Diseño completamente responsivo</em>
</div>

## 📝 Nota Académica

> **Proyecto Educativo - Bootcamp de Inteligencia Artificial Factoría F5**
> 
> Este es un proyecto académico con fines educativos únicamente. El diseño está inspirado en los portales de la Comunidad de Madrid pero no está afiliado ni representa a ninguna institución oficial.

## 🌐 Demo en Vivo

🚀 **Aplicación desplegada**: [https://student-predictor-oelj.onrender.com/](https://student-predictor-oelj.onrender.com/)

*Nota: El despliegue en Render puede tardar unos segundos en cargar debido al plan gratuito.*

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
├── 📱 client/                              # Frontend React + Tailwind
│   ├── public/
│   ├── src/
│   │   ├── components/                     # Componentes React reutilizables
│   │   │   ├── Button.jsx                  # Botón personalizado con estilos
│   │   │   ├── Navbar.jsx                  # Navegación principal
│   │   │   ├── Footer.jsx                  # Pie de página
│   │   │   ├── StudentPredictionForm.jsx   # Formulario de predicción
│   │   │   └── PredictionList.jsx          # Lista de predicciones históricas
│   │   │
│   │   ├── pages/                          # Páginas principales
│   │   │   ├── Prediction.jsx              # Página de nueva predicción
│   │   │   └── Monitoring.jsx              # Dashboard de seguimiento
│   │   │
│   │   ├── services/                       # Comunicación con API
│   │   │   └── studentService.js           # Servicio HTTP para backend
│   │   │
│   │   ├── routes/                         # Configuración de rutas
│   │   │   └── Routes.jsx                  # React Router setup
│   │   │
│   │   ├── layout/                         # Layout general
│   │   │   └── layout.jsx                  # Estructura común (navbar+footer)
│   │   │
│   │   └── assets/                         # Recursos estáticos
│   │       └── images/                     # Imágenes del proyecto
│   │
│   ├── package.json                        # Dependencias React
│   ├── tailwind.config.js                  # Configuración Tailwind CSS
│   └── vite.config.js                      # Configuración Vite
│
├── 🐍 server/                              # Backend Python + FastAPI
│   ├── database/                           # Gestión de base de datos
│   │   ├── supabase_client.py              # Cliente Supabase
│   │   └── migrations.py                   # Sistema de migración de BD
│   │
│   ├── models/                             # Machine Learning & Datos
│   │   ├── model_trainer.py                # Entrenamiento XGBoost
│   │   ├── predictor.py                    # Lógica de predicción ML
│   │   ├── preprocessing.py                # Pipeline de preprocesamiento
│   │   ├── schemas.py                      # Validación Pydantic
│   │   └── checking_data.ipynb             # Análisis exploratorio
│   │
│   ├── tests/                              # Tests unitarios
│   │   ├── test_predictor.py               # Tests del modelo ML
│   │   ├── test_preprocessing.py           # Tests del pipeline
│   │   └── test_migrations.py              # Tests de BD
│   │
│   ├── artifacts/                          # Modelos entrenados (generados)
│   │   ├── xgboost_multiclass_model.pkl    # Modelo XGBoost serializado
│   │   └── xgboost_multiclass_pipeline.pkl # Pipeline preprocesamiento
│   │
│   └── main.py                             # API FastAPI principal
│
├── 📊 data/                                # Datasets
│   ├── raw/
│   │   └── raw_data.csv                    # Datos originales
│   └── processed/
│       └── dataset_procesado.csv           # Datos limpios para ML
│
├── 🐳 Docker & Deploy/                     # Configuración deployment
│   ├── Dockerfile.backend                  # Contenedor Python/FastAPI
│   ├── Dockerfile.frontend                 # Contenedor React/Nginx
│   ├── docker-compose.yml                 # Orquestación completa
│   ├── nginx.conf                          # Configuración Nginx
│   ├── render-backend.yaml                # Deploy backend Render
│   └── render-frontend.yaml               # Deploy frontend Render
│
├── 🔧 Configuración/
│   ├── requirements.txt                    # Dependencias Python
│   ├── pyproject.toml                      # Configuración proyecto Python
│   ├── .env_example                        # Variables de entorno ejemplo
│   ├── .gitignore                          # Archivos ignorados Git
│   └── init_database.py                    # Script inicialización BD
│
└── 📖 README.md                            # Documentación principal
```

## 🛠️ Tecnologías Utilizadas

### Backend
- Python 3.13+
- XGBoost
- Scikit-learn
- FastAPI
- Supabase

### Frontend
- React
- Tailwind CSS
- Vite

## 📋 Requisitos Previos

- Python 3.13 o superior
- Node.js y npm
- Git

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone [URL del repositorio]
cd Multiclass_Clasification
```

### 2. Configuración del Backend

#### 2.1. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

#### 2.2. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 2.3. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
cp .env_example .env
# Editar .env con tus credenciales de Supabase
```

### 3. Preparación de Datos y Modelo

#### 3.1. Crear estructura de carpetas
```bash
mkdir -p data/raw data/processed
```

#### 3.2. Descargar y colocar el dataset
- Descargar el dataset de [Predict students' dropout and academic success](https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention)
- Colocar el archivo como `data/raw/raw_data.csv`

#### 3.3. Entrenar el modelo ML
```bash
python server/models/model_trainer.py
```

#### 3.4. Inicializar la base de datos
```bash
python init_database.py
```

### 4. Levantar el Backend
```bash
uvicorn server.main:app --reload
```

### 5. Configuración del Frontend

#### 5.1. Instalar dependencias
```bash
cd client
npm install
```

#### 5.2. Ejecutar en modo desarrollo
```bash
npm run dev
```

### Ejecutar Tests 
 ```bash
   pytest server/tests
   ```

## 🐳 Ejecución con Docker (Opcional)

Si prefieres usar Docker:

```bash
# Configurar variables de entorno
cp .env_example .env

# Ejecutar con Docker Compose
docker-compose up --build
```

## 🔍 Verificación del Sistema

Una vez completada la instalación:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Estado del modelo**: http://localhost:8000/model/status  
- **Ver estudiantes**: http://localhost:8000/students

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
