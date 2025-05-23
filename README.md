# Sistema de Clasificación Multiclase para Predicción de Éxito Académico

## 📚 Descripción del Proyecto

Este proyecto implementa un sistema de clasificación multiclase para predecir el éxito académico de estudiantes universitarios. El sistema puede clasificar a los estudiantes en tres categorías:
- Dropout (Abandono)
- Graduate (Graduado)
- Enrolled (Matriculado)

Utiliza técnicas avanzadas de aprendizaje automático, específicamente XGBoost y Random Forest, para realizar predicciones basadas en diversos factores académicos y socioeconómicos.

## 🏗️ Estructura del Proyecto

```
├── client/                  # Frontend de la aplicación
│   ├── src/                 # Código fuente React
│   └── public/              # Archivos estáticos
├── data/                    # Conjuntos de datos
│   ├── raw/                 # Datos sin procesar
│   └── processed/           # Datos procesados
├── server/                  # Backend de la aplicación
│   ├── models/              # Modelos ML y preprocesamiento
│   ├── database/            # Configuración de base de datos
│   └── src/                 # Lógica del servidor
├── model_training/          # Notebooks de entrenamiento
│   ├── random_forest.ipynb
│   └── xgboost.ipynb
└── notebooks/              # Notebooks de análisis
    ├── EDA.ipynb           # Análisis exploratorio de datos
    └── data_cleaning.ipynb # Limpieza y preprocesamiento de datos
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

### Preparación de Datos

1. Crear las carpetas necesarias para los datos:
```bash
mkdir -p data/raw data/processed
```

2. Colocar el archivo CSV con los datos del estudiante en la carpeta correspondiente:
- Datos sin procesar: `data/raw/student_data.csv`
- Datos procesados: `data/processed/processed_data.csv`

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
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

### Frontend

1. Navegar al directorio del cliente:
```bash
cd client
```

2. Instalar dependencias:
```bash
npm install
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
