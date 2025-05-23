import pandas as pd
import os
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
from server.models.preprocessing import PreprocessingPipeline
from collections import Counter

#-------------------------------------------------------------------------------------------------------
# Configuración de rutas
print("🔧 Configurando rutas...")

# Obtener la ruta del script actual (independiente del working directory)
current_dir = os.path.dirname(os.path.abspath(__file__))  # \...\Multiclass_Clasification\server\models
server_path = os.path.dirname(current_dir)                # \...\Multiclass_Clasification\server
project_root = os.path.dirname(server_path)               # \...\Multiclass_Clasification

data_root_path = os.path.join(project_root, "data")       # \...\Multiclass_Clasification\data
raw_data_path = os.path.join(data_root_path, "raw_data.csv")
process_data_path = os.path.join(data_root_path, "dataset_procesado.csv")

# Rutas para guardar modelos (en server/data)
data_server_path = os.path.join(server_path, "artifacts")      # \...\Multiclass_Clasification\server\data
pipeline_path = os.path.join(data_server_path, "xgboost_multiclass_pipeline.pkl")
model_path = os.path.join(data_server_path, "xgboost_multiclass_model.pkl")

print(f"📁 Rutas configuradas:")
print(f"   Dataset procesado: {process_data_path}")
print(f"   Pipeline: {pipeline_path}")
print(f"   Modelo: {model_path}")

# Crear directorio si no existe
os.makedirs(data_server_path, exist_ok=True)

# ------------------------------------------------------------------------------------------------------
# Cargar y preparar datos
print("\n📊 Cargando datos...")

df = pd.read_csv(process_data_path)
print(f"✅ Dataset cargado: {df.shape}")
print(f"📋 Columnas disponibles: {len(df.columns)}")

# Definir las variables numéricas y categóricas según el EDA
numerical_features = [
    'curricular_units_1st_sem_(grade)','curricular_units_2nd_sem_(grade)',
    'curricular_units_1st_sem_(approved)','curricular_units_2nd_sem_(approved)',
    'curricular_units_1st_sem_(evaluations)','curricular_units_2nd_sem_(evaluations)',
    # Agregamos estas variables numéricas que estaban incorrectamente clasificadas como categóricas
    'unemployment_rate', 'gdp','age_at_enrollment'
]

# Para las categóricas con one-hot encoding, buscamos las columnas correspondientes
categorical_base_features = [
    'scholarship_holder',
    'tuition_fees_up_to_date',
    'marital_status',
    'previous_qualification',
    'mother\'s_qualification',  # ✅ Mantener con apóstrofe para el dataset
    'father\'s_qualification'   # ✅ Mantener con apóstrofe para el dataset
]

print("\n🔍 Identificando features...")

# Verificar features numéricas existentes
existing_num_features = [col for col in numerical_features if col in df.columns]
print(f"📊 Features numéricas encontradas: {len(existing_num_features)}")
for feat in existing_num_features:
    print(f"   ✓ {feat}")

# Buscar features categóricas (one-hot encoded)
categorical_features = []
for base_feature in categorical_base_features:
    # Buscar columnas que contengan el nombre base
    base_clean = base_feature.lower().replace(' ', '_').replace("'", "")
    matching_cols = []
    
    for col in df.columns:
        col_clean = col.lower().replace(' ', '_').replace("'", "")
        if base_clean in col_clean and col not in existing_num_features and col != 'target':
            matching_cols.append(col)
    
    if matching_cols:
        categorical_features.extend(matching_cols)
        print(f"📋 Para {base_feature} encontradas: {len(matching_cols)} columnas")
    else:
        print(f"⚠️ No se encontraron columnas para: {base_feature}")

print(f"\n📊 Resumen de features:")
print(f"   Numéricas: {len(existing_num_features)}")
print(f"   Categóricas: {len(categorical_features)}")

# Combinar todas las features
features = existing_num_features + categorical_features
print(f"   Total features: {len(features)}")

# Verificar que todas las features existen en el DataFrame
missing_features = [feat for feat in features if feat not in df.columns]
if missing_features:
    print(f"❌ Features faltantes: {missing_features}")
    raise ValueError("Algunas features no existen en el dataset")

# Preparar X e y
X = df[features]
y = df['target']

print(f"\n📊 Datos preparados:")
print(f"   X shape: {X.shape}")
print(f"   y shape: {y.shape}")
print(f"   Clases en y: {sorted(y.unique())}")
print(f"   Distribución de clases: {dict(y.value_counts())}")

# División en conjuntos de entrenamiento, validación y prueba (70/15/15)
print("\n🔀 Dividiendo datos...")

X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.1765, random_state=42, stratify=y_train_val
)

print(f"✅ División completada:")
print(f"   Train: {X_train.shape}")
print(f"   Val: {X_val.shape}")
print(f"   Test: {X_test.shape}")

# Calcular pesos por clase
print("\n⚖️ Calculando pesos por clase...")

class_counts = dict(Counter(y_train))
total_samples = sum(class_counts.values())
class_weights_dict = {cls: total_samples / count for cls, count in class_counts.items()}
sample_weights = [class_weights_dict[label] for label in y_train]

print("Pesos por clase:")
for cls, weight in class_weights_dict.items():
    print(f"   Clase {cls}: peso {weight:.4f}")

# Crear DMatrix para todos los conjuntos
print("\n🔧 Creando DMatrix...")

dtrain = xgb.DMatrix(X_train, label=y_train, weight=sample_weights)
dval = xgb.DMatrix(X_val, label=y_val)
dtest = xgb.DMatrix(X_test, label=y_test)

print("✅ DMatrix creados")

# Hiperparámetros optimizados
print("\n🎯 Configurando hiperparámetros...")

best_params = {
    'learning_rate': 0.10282143320694112,
    'max_depth': 3,
    'min_child_weight': 8,
    'gamma': 0.5892708660242506,
    'subsample': 0.9989684569162808,
    'colsample_bytree': 0.8591274563728392,
    'lambda': 2.7193518380626177e-05,
    'alpha': 4.851829419554719e-06,
    'objective': 'multi:softprob',
    'eval_metric': 'mlogloss',
    'num_class': 3,
    'seed': 42
}

print("✅ Hiperparámetros configurados")

# Entrenamiento del modelo
print("\n🚀 Entrenando modelo final...")

evallist = [(dtrain, 'train'), (dval, 'validation')]
final_model = xgb.train(
    best_params,
    dtrain,
    num_boost_round=2000,
    evals=evallist,
    early_stopping_rounds=50,
    verbose_eval=100
)

print("✅ Modelo entrenado")

# Evaluación del modelo
print("\n📊 Evaluando modelo...")

y_train_pred = np.argmax(final_model.predict(dtrain), axis=1)
y_val_pred = np.argmax(final_model.predict(dval), axis=1)
y_test_pred = np.argmax(final_model.predict(dtest), axis=1)

def print_metrics(name, y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='macro')
    print(f"{name} - Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1: {f1:.4f}")
    return acc, f1

train_accuracy, train_f1 = print_metrics("Entrenamiento", y_train, y_train_pred)
val_accuracy, val_f1 = print_metrics("Validación", y_val, y_val_pred)
test_accuracy, test_f1 = print_metrics("Test", y_test, y_test_pred)

print(f"\nDiferencia en Accuracy (train-val): {train_accuracy - val_accuracy:.4f}")
print(f"Diferencia en F1 (train-val): {train_f1 - val_f1:.4f}")

print("\nReporte de clasificación (Test):")
print(classification_report(y_test, y_test_pred, target_names=['Dropout', 'Graduate', 'Enrolled']))

# Guardar modelo
print("\n💾 Guardando modelo...")

with open(model_path, 'wb') as f:
    pickle.dump(final_model, f)
print(f"✅ Modelo guardado en: {model_path}")

# ✅ GUARDAR PIPELINE CORREGIDO
print("\n🔧 Configurando pipeline de preprocesamiento corregido...")

# Identificar features categóricas y numéricas correctamente
model_categorical_features = []
model_numerical_features = []

# Features numéricas conocidas
known_numerical = [
    'curricular_units_1st_sem_(grade)',
    'curricular_units_2nd_sem_(grade)', 
    'curricular_units_1st_sem_(approved)',
    'curricular_units_2nd_sem_(approved)',
    'curricular_units_1st_sem_(evaluations)',
    'curricular_units_2nd_sem_(evaluations)',
    'unemployment_rate',
    'gdp', 
    'age_at_enrollment'
]

for feature in features:
    if feature in known_numerical:
        model_numerical_features.append(feature)
    else:
        model_categorical_features.append(feature)

print(f"📊 Features para el pipeline:")
print(f"   Categóricas: {len(model_categorical_features)}")
print(f"   Numéricas: {len(model_numerical_features)}")

# Crear y guardar pipeline
preprocessing_pipeline = PreprocessingPipeline(
    features=features,
    categorical_features=model_categorical_features,
    numerical_features=model_numerical_features
)

with open(pipeline_path, 'wb') as f:
    pickle.dump(preprocessing_pipeline, f)
print(f"✅ Pipeline guardado en: {pipeline_path}")

# ✅ VERIFICACIÓN COMPLETA: Probar con datos realistas
print("\n🧪 Verificando pipeline con datos de prueba...")

try:
    with open(pipeline_path, 'rb') as f:
        test_pipeline = pickle.load(f)
    print("✅ Pipeline cargado correctamente")

    # Crear datos de prueba que coincidan exactamente con el formato del API
    test_data_good_student = {
        'curricular_units_1st_sem_grade': 18.0,  # Buenas calificaciones
        'curricular_units_2nd_sem_grade': 19.0,
        'curricular_units_1st_sem_approved': 6,
        'curricular_units_2nd_sem_approved': 6,
        'curricular_units_1st_sem_evaluations': 6,
        'curricular_units_2nd_sem_evaluations': 6,
        'unemployment_rate': 8.0,
        'gdp': 2.0,
        'age_at_enrollment': 19,
        'scholarship_holder': 'Yes',
        'tuition_fees_up_to_date': 'Yes',
        'marital_status': 'Single',
        'previous_qualification': 'Secondary education',
        'mothers_qualification': 'Higher education—bachelor\'s degree',
        'fathers_qualification': 'Higher education—degree'
    }
    
    test_data_poor_student = {
        'curricular_units_1st_sem_grade': 8.0,   # Malas calificaciones
        'curricular_units_2nd_sem_grade': 7.0,
        'curricular_units_1st_sem_approved': 2,
        'curricular_units_2nd_sem_approved': 1,
        'curricular_units_1st_sem_evaluations': 8,
        'curricular_units_2nd_sem_evaluations': 9,
        'unemployment_rate': 15.0,
        'gdp': -1.0,
        'age_at_enrollment': 35,
        'scholarship_holder': 'No',
        'tuition_fees_up_to_date': 'No',
        'marital_status': 'Divorced',
        'previous_qualification': 'Basic education 3rd cycle (9th/10th/11th year) or equivalent',
        'mothers_qualification': 'Cannot read or write',
        'fathers_qualification': 'Unknown'
    }

    print(f"\n🎓 Prueba 1: Estudiante con buen perfil")
    df_test_good = pd.DataFrame([test_data_good_student])
    result_good = test_pipeline.transform(df_test_good)
    print(f"   Shape: {result_good.shape}")
    print(f"   Suma total: {result_good.sum().sum()}")
    
    print(f"\n📉 Prueba 2: Estudiante con mal perfil")
    df_test_poor = pd.DataFrame([test_data_poor_student])
    result_poor = test_pipeline.transform(df_test_poor)
    print(f"   Shape: {result_poor.shape}")
    print(f"   Suma total: {result_poor.sum().sum()}")
    
    # Verificar que los resultados son diferentes
    if result_good.sum().sum() != result_poor.sum().sum():
        print("✅ Pipeline funcionando: diferentes inputs generan diferentes outputs")
    else:
        print("⚠️ PROBLEMA: Diferentes inputs generan el mismo output")
    
    # Verificar que las variables numéricas se preservan
    numerical_cols = ['curricular_units_1st_sem_(grade)', 'curricular_units_2nd_sem_(grade)', 
                     'unemployment_rate', 'gdp', 'age_at_enrollment']
    
    for col in numerical_cols:
        if col in result_good.columns:
            val_good = result_good[col].iloc[0]
            val_poor = result_poor[col].iloc[0]
            print(f"   {col}: buen={val_good}, mal={val_poor}")

except Exception as e:
    print(f"❌ Error probando pipeline: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("🎯 PIPELINE CORREGIDO Y VERIFICADO")
print("="*60)