import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, learning_curve, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Cargar los datos
df = pd.read_csv('../../../data/processed/dataset_procesado.csv')

# Separar características (X) y variable objetivo (y)
X = df.drop('target', axis=1)
y = df['target']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Escalar las características
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Definir los parámetros para la búsqueda en cuadrícula
param_grid = {
    'C': [0.00001, 0.0001, 0.001],
    'gamma': [0.00001, 0.0001, 0.001],
    'kernel': ['linear'],
    'class_weight': ['balanced'], 
    'shrinking': [True],
    'tol': [1e-4, 1e-3]
}

# Crear el modelo base
base_model = SVC(random_state=42, cache_size=2000)

# Realizar búsqueda en cuadrícula con validación cruzada
grid_search = GridSearchCV(
    base_model,
    param_grid,
    cv=5,
    scoring='accuracy',
    n_jobs=-1,
    verbose=1
)

# Ajustar el modelo con búsqueda en cuadrícula
grid_search.fit(X_train_scaled, y_train)

# Obtener el mejor modelo
svm_model = grid_search.best_estimator_

# Imprimir los mejores parámetros
print("\nMejores parámetros encontrados:")
print(grid_search.best_params_)

# Realizar predicciones
y_pred = svm_model.predict(X_test_scaled)

# Obtener la precisión del modelo en conjunto de entrenamiento
train_accuracy = svm_model.score(X_train_scaled, y_train)
# Obtener la precisión del modelo en conjunto de prueba
test_accuracy = svm_model.score(X_test_scaled, y_test)

print("\nAnálisis de Overfitting:")
print("-" * 50)
print("Precisión en conjunto de entrenamiento:", round(train_accuracy * 100, 2), "%")
print("Precisión en conjunto de prueba:", round(test_accuracy * 100, 2), "%")
print("Diferencia (train-test):", round((train_accuracy - test_accuracy) * 100, 2), "%")

if train_accuracy - test_accuracy > 0.1:
    print("\n⚠️ ADVERTENCIA: Posible overfitting detectado")
    print("La diferencia entre precisión de entrenamiento y prueba es mayor al 10%")
elif train_accuracy - test_accuracy < 0.05:
    print("\n✅ Modelo bien ajustado")
    print("La diferencia entre precisión de entrenamiento y prueba es menor al 5%")
else:
    print("\n⚠️ Ligero overfitting")
    print("La diferencia entre precisión de entrenamiento y prueba está entre 5-10%")

# Calcular curvas de aprendizaje
train_sizes, train_scores, test_scores = learning_curve(
    svm_model, X_train_scaled, y_train,
    train_sizes=np.linspace(0.1, 1.0, 10),
    cv=5, n_jobs=-1)

# Calcular medias y desviaciones estándar
train_mean = np.mean(train_scores, axis=1)
train_std = np.std(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)
test_std = np.std(test_scores, axis=1)

# Graficar curvas de aprendizaje
plt.figure(figsize=(10, 6))
plt.plot(train_sizes, train_mean, label='Precisión entrenamiento', color='blue', marker='o')
plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, alpha=0.15, color='blue')
plt.plot(train_sizes, test_mean, label='Precisión validación', color='green', marker='o')
plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, alpha=0.15, color='green')
plt.xlabel('Tamaño del conjunto de entrenamiento')
plt.ylabel('Precisión')
plt.title('Curvas de Aprendizaje - SVM')
plt.legend(loc='lower right')
plt.grid(True)
plt.show()

# Evaluar el modelo
print("\nReporte de Clasificación:")
print(classification_report(y_test, y_pred))

# Crear matriz de confusión
cm = confusion_matrix(y_test, y_pred)

# Visualizar matriz de confusión
plt.figure(figsize=(10,8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusión - SVM')
plt.ylabel('Valores Reales')
plt.xlabel('Predicciones')
plt.show()

# Guardar el modelo
modelo_path = '../../../models/svm_model.pkl'
with open(modelo_path, 'wb') as file:
    pickle.dump(svm_model, file)
print(f"\nModelo guardado en: {modelo_path}")