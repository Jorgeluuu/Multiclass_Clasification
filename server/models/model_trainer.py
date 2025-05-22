# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# import joblib
# import os
import pandas as pd
import os
import numpy as np
import pickle
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from sklearn.metrics import classification_report, roc_auc_score, roc_curve
from preprocessing import PreprocessingPipeline
from collections import Counter



#-------------------------------------------------------------------------------------------------------
# Obtener la ruta del script actual (independiente del working directory)
current_dir = os.path.dirname(os.path.abspath(__file__))  # \...\Multiclass_Clasification\server\models
server_path = os.path.dirname(current_dir)                # \...\Multiclass_Clasification\server
project_root = os.path.dirname(server_path)               # \...\Multiclass_Clasification

data_root_path = os.path.join(project_root, "data")       # \...\Multiclass_Clasification\data
raw_data_path = os.path.join(data_root_path, "raw_data.csv")
process_data_path = os.path.join(data_root_path, "dataset_procesado.csv")

# Rutas para guardar modelos (en server/data)
data_server_path = os.path.join(server_path, "data")      # \...\Multiclass_Clasification\server\data
pipeline_path = os.path.join(data_server_path, "xgboost_multiclass_pipeline.pkl")
model_path = os.path.join(data_server_path, "xgboost_multiclass_model.pkl")
# ------------------------------------------------------------------------------------------------------

df = pd.read_csv(process_data_path)

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
    'mother\'s_qualification',
    'father\'s_qualification'
]

existing_num_features = [col for col in numerical_features if col in df.columns]

categorical_features = []
for base_feature in categorical_base_features:
    matching_cols = [col for col in df.columns if base_feature.lower().replace(' ', '_') in col.lower()]
    if matching_cols:
        categorical_features.extend(matching_cols)

features = existing_num_features + categorical_features


# Preparar X e y
X = df[features]
y = df['target']

# División en conjuntos de entrenamiento, validación y prueba (70/15/15)
X_train_val, X_test, y_train_val, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train_val, y_train_val, test_size=0.1765, random_state=42, stratify=y_train_val
)


# Pesos por clase
class_counts = dict(Counter(y_train))
total_samples = sum(class_counts.values())
class_weights_dict = {cls: total_samples / count for cls, count in class_counts.items()}
sample_weights = [class_weights_dict[label] for label in y_train]

print("Pesos por clase:")
for cls, weight in class_weights_dict.items():
    print(f"Clase {cls}: peso {weight:.4f}")

# Crear DMatrix para todos los conjuntos
dtrain = xgb.DMatrix(X_train, label=y_train, weight=sample_weights)
dval = xgb.DMatrix(X_val, label=y_val)
dtest = xgb.DMatrix(X_test, label=y_test)

# Hiparparámetros
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


# Entrenamiento
print("Entrenando modelo final con hiperparámetros optimizados...")
evallist = [(dtrain, 'train'), (dval, 'validation')]
final_model = xgb.train(
    best_params,
    dtrain,
    num_boost_round=2000,
    evals=evallist,
    early_stopping_rounds=50,
    verbose_eval=100
)

# Evaluación
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
with open(model_path, 'wb') as f:
    pickle.dump(final_model, f)
print(f"\nModelo guardado en: {model_path}")

# Guardar pipeline
categorical_features = [col for col in features if '_' in col]
numerical_features = [col for col in features if '_' not in col]

preprocessing_pipeline = PreprocessingPipeline(
    features=features,
    categorical_features=categorical_features,
    numerical_features=numerical_features
)
with open(pipeline_path, 'wb') as f:
    pickle.dump(preprocessing_pipeline, f)
print(f"Pipeline de preprocesamiento guardado en: {pipeline_path}")

# -------------------------------------------------------------------------------------------------------
# # Lista de evaluaciones para monitorear
# evallist = [(dtrain, 'train'), (dval, 'validation')]

# # Entrenamiento del modelo final con early stopping
# print("Entrenando modelo final con hiperparámetros optimizados...")
# num_rounds = 2000  # Aumentamos para asegurar convergencia
# final_model = xgb.train(
#     best_params, 
#     dtrain, 
#     num_rounds, 
#     evallist, 
#     early_stopping_rounds=50,
#     verbose_eval=100
# )

# # Predicciones en todos los conjuntos
# y_train_pred = np.argmax(final_model.predict(dtrain), axis=1)
# y_val_pred = np.argmax(final_model.predict(dval), axis=1)
# y_test_pred = np.argmax(final_model.predict(dtest), axis=1)


# # Entrenamiento
# train_accuracy = accuracy_score(y_train, y_train_pred)
# train_precision, train_recall, train_f1, _ = precision_recall_fscore_support(
#     y_train, y_train_pred, average='macro')

# # Validación
# val_accuracy = accuracy_score(y_val, y_val_pred)
# val_precision, val_recall, val_f1, _ = precision_recall_fscore_support(
#     y_val, y_val_pred, average='macro')

# # Test
# test_accuracy = accuracy_score(y_test, y_test_pred)
# test_precision, test_recall, test_f1, _ = precision_recall_fscore_support(
#     y_test, y_test_pred, average='macro')


# print(f"Entrenamiento - Accuracy: {train_accuracy:.4f}, Precision: {train_precision:.4f}, Recall: {train_recall:.4f}, F1: {train_f1:.4f}")
# print(f"Validación - Accuracy: {val_accuracy:.4f}, Precision: {val_precision:.4f}, Recall: {val_recall:.4f}, F1: {val_f1:.4f}")
# print(f"Test - Accuracy: {test_accuracy:.4f}, Precision: {test_precision:.4f}, Recall: {test_recall:.4f}, F1: {test_f1:.4f}")

# # Evaluar overfitting
# train_val_acc_diff = train_accuracy - val_accuracy
# train_val_f1_diff = train_f1 - val_f1

# print(f"\nDiferencia en Accuracy (train-val): {train_val_acc_diff:.4f} ({train_val_acc_diff*100:.2f}%)")
# print(f"Diferencia en F1 (train-val): {train_val_f1_diff:.4f} ({train_val_f1_diff*100:.2f}%)")

# # Mostrar reporte de clasificación detallado para test
# print("\nReporte de clasificación (Test):")
# print(classification_report(y_test, y_test_pred, 
#                            target_names=['Dropout', 'Graduate', 'Enrolled']))



# # Guardar el modelo final

# with open(model_path, 'wb') as model_file:
#     pickle.dump(final_model, model_file)
# print(f"\nModelo guardado en: {model_path}")

# # Guardar pipeline de preprocesamiento
# class PreprocessingPipeline:
#     def __init__(self, features, categorical_features=None, numerical_features=None):
#         self.features = features
#         self.categorical_features = categorical_features or []
#         self.numerical_features = numerical_features or []
        
#         # Extraer las categorías base (sin los sufijos)
#         self.categorical_bases = []
#         for feature in self.categorical_features:
#             base = feature.split('_')[0]
#             if base not in self.categorical_bases:
#                 self.categorical_bases.append(base)
        
#     def transform(self, X):
#         """
#         Preprocesa nuevos datos para predicción, incluyendo one-hot encoding
        
#         Args:
#             X: DataFrame con los datos de entrada (sin one-hot encoding)
            
#         Returns:
#             DataFrame con las características seleccionadas y transformadas
#         """
#         # Copia para no modificar los datos originales
#         X_processed = X.copy()
        
#         # Aplicar one-hot encoding a variables categóricas
#         for base_feature in self.categorical_bases:
#             if base_feature in X_processed.columns:
#                 # Extraer el valor categórico
#                 value = X_processed[base_feature].iloc[0]
                
#                 # Crear la columna one-hot correspondiente
#                 for cat_feature in self.categorical_features:
#                     if cat_feature.startswith(base_feature + '_'):
#                         # Extraer el valor después del guion bajo
#                         feature_value = cat_feature.split('_', 1)[1]
                        
#                         # Establecer 1 si coincide, 0 en caso contrario
#                         X_processed[cat_feature] = 1 if str(value) == feature_value else 0
                
#                 # Eliminar la columna original
#                 X_processed = X_processed.drop(base_feature, axis=1)
        
#         # Verificar que todas las características necesarias estén presentes
#         missing_features = set(self.features) - set(X_processed.columns)
#         if missing_features:
#             # Añadir columnas faltantes con valores 0 (caso de categorías no presentes)
#             for feature in missing_features:
#                 X_processed[feature] = 0
        
#         # Seleccionar solo las características relevantes en el orden correcto
#         return X_processed[self.features]
    
#     def fit_transform(self, X, y=None):
#         """
#         Para mantener compatibilidad con la API de sklearn
#         """
#         return self.transform(X)

# # Crear una instancia del pipeline con información sobre características
# categorical_features = [col for col in features if '_' in col]
# numerical_features = [col for col in features if '_' not in col]

# preprocessing_pipeline = PreprocessingPipeline(
#     features=features,
#     categorical_features=categorical_features,
#     numerical_features=numerical_features
# )


# # Guardar el pipeline de preprocesamiento

# with open(pipeline_path, 'wb') as pipeline_file:
#     pickle.dump(preprocessing_pipeline, pipeline_file)

# print(f"Pipeline de preprocesamiento guardado en: {pipeline_path}")

# -------------------------------------------------------------------------------------------------------

# # # DATOS FAKE PARA TESTEAR EL BACK
# data = {
#     'age': [18, 22, 25, 30, 35, 40],
#     'education_years': [12, 14, 16, 18, 20, 22],
#     'credits_failed': [0, 2, 1, 3, 0, 4],
#     'target': ['Graduate', 'Enrolled', 'Dropout', 'Graduate', 'Dropout', 'Enrolled']
# }

# df = pd.DataFrame(data)

# X = df.drop('target', axis=1)
# y = df['target']
# # -------------------------------------------------------------------------------------------------------
# # Entrenar el modelo
# model = RandomForestClassifier(random_state=42) # Añadir random_state para reproducibilidad
# model.fit(X, y)
# # -------------------------------------------------------------------------------------------------------
# # El pkl se guarda en la misma carpeta que este script
# model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
# joblib.dump(model, model_path)
# print(f"✅ Modelo de prueba guardado como {model_path}")