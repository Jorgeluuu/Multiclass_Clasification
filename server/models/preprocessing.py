import pandas as pd
import os

class PreprocessingPipeline:
    def __init__(self, features, categorical_features=None, numerical_features=None):
        self.features = features
        self.categorical_features = categorical_features or []
        self.numerical_features = numerical_features or []
        
        # Mapear nombres de campo del API a nombres del dataset
        self.field_mapping = {
            'mothers_qualification': "mother's_qualification",
            'fathers_qualification': "father's_qualification"
        }
        
        print(f"🏗️ Pipeline inicializado con:")
        print(f"   Features totales: {len(self.features)}")
        print(f"   Categóricas: {len(self.categorical_features)}")
        print(f"   Numéricas: {len(self.numerical_features)}")
    
    def transform(self, X):
        """
        Transforma los datos de entrada al formato esperado por el modelo
        """
        print(f"\n📥 Input DataFrame:")
        print(f"   Shape: {X.shape}")
        print(f"   Columns: {list(X.columns)}")
        
        X_processed = X.copy()
        
        # 1. Mapear nombres de campos si es necesario
        for api_field, dataset_field in self.field_mapping.items():
            if api_field in X_processed.columns:
                X_processed[dataset_field] = X_processed[api_field]
                X_processed.drop(api_field, axis=1, inplace=True)
                print(f"🔄 Mapeado {api_field} → {dataset_field}")
        
        print(f"\n🔧 Procesando variables categóricas...")
        
        # 2. Procesar variables categóricas con one-hot encoding
        for feature in self.categorical_features:
            if '_' in feature:  # Es una columna one-hot encoded
                # Ejemplo: "scholarship_holder_Yes" -> base="scholarship_holder", value="Yes"
                parts = feature.split('_', 1)
                if len(parts) == 2:
                    base_name, expected_value = parts
                else:
                    continue
                
                # Buscar la columna original (puede tener apóstrofes)
                original_col = None
                for col in X_processed.columns:
                    # Comparar eliminando espacios, apóstrofes y convirtiendo a minúsculas
                    col_clean = col.replace("'", "").replace(" ", "_").lower()
                    base_clean = base_name.replace("'", "").replace(" ", "_").lower()
                    
                    if col_clean == base_clean:
                        original_col = col
                        break
                
                if original_col and original_col in X_processed.columns:
                    actual_value = str(X_processed[original_col].iloc[0])
                    
                    # Crear columna one-hot - comparación directa
                    X_processed[feature] = 1 if actual_value == expected_value else 0
                    print(f"✅ {feature} = {X_processed[feature].iloc[0]} | '{actual_value}' == '{expected_value}' ?")
                else:
                    # Si no encontramos la columna original, poner 0
                    X_processed[feature] = 0
                    print(f"❌ No encontrada base para {feature}, asignando 0")
        
        # 3. Eliminar columnas categóricas originales
        columns_to_drop = []
        for col in X_processed.columns:
            # Si es una columna categórica original y no está en features finales
            if col not in self.features and (
                any(col.replace("'", "").replace(" ", "_").lower() == 
                    cat_feat.split('_')[0].replace("'", "").replace(" ", "_").lower() 
                    for cat_feat in self.categorical_features if '_' in cat_feat)
            ):
                columns_to_drop.append(col)
        
        for col in columns_to_drop:
            X_processed.drop(col, axis=1, inplace=True)
            print(f"🗑️ Eliminada columna original: {col}")
        
        print(f"\n🔧 Procesando variables numéricas...")
        
        # 4. Mapear variables numéricas con nombres diferentes
        numerical_mapping = {
            'curricular_units_1st_sem_grade': 'curricular_units_1st_sem_(grade)',
            'curricular_units_2nd_sem_grade': 'curricular_units_2nd_sem_(grade)',
            'curricular_units_1st_sem_approved': 'curricular_units_1st_sem_(approved)',
            'curricular_units_2nd_sem_approved': 'curricular_units_2nd_sem_(approved)',
            'curricular_units_1st_sem_evaluations': 'curricular_units_1st_sem_(evaluations)',
            'curricular_units_2nd_sem_evaluations': 'curricular_units_2nd_sem_(evaluations)'
        }
        
        for api_name, dataset_name in numerical_mapping.items():
            if api_name in X_processed.columns and dataset_name in self.features:
                X_processed[dataset_name] = X_processed[api_name]
                X_processed.drop(api_name, axis=1, inplace=True)
                print(f"✅ Mapeado numérico: {api_name} → {dataset_name} = {X_processed[dataset_name].iloc[0]}")
        
        # 5. Añadir columnas faltantes con valor 0
        missing_features = set(self.features) - set(X_processed.columns)
        for feature in missing_features:
            X_processed[feature] = 0
            print(f"➕ Añadida feature faltante: {feature} = 0")
        
        # 6. Asegurar orden correcto de columnas
        result = X_processed[self.features]
        
        print(f"\n📤 Resultado final:")
        print(f"   Shape: {result.shape}")
        print(f"   Features: {len(result.columns)}")
        
        # Mostrar resumen de valores no-cero
        non_zero_features = {}
        for col in result.columns:
            val = result[col].iloc[0]
            if val != 0:
                non_zero_features[col] = val
        
        print(f"   Features no-cero ({len(non_zero_features)}):")
        for feat, val in list(non_zero_features.items())[:10]:  # Mostrar solo los primeros 10
            print(f"     {feat}: {val}")
        if len(non_zero_features) > 10:
            print(f"     ... y {len(non_zero_features) - 10} más")
        
        print(f"   Suma total: {result.sum().sum()}")
        
        return result
    
    def fit_transform(self, X, y=None):
        return self.transform(X)