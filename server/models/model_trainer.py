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
from server.models.preprocessing import PreprocessingPipeline
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

