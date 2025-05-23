import pandas as pd
import os

class PreprocessingPipeline:
    def __init__(self, features, categorical_features=None, numerical_features=None):
        self.features = features
        
        # ✅ CORREGIR: Auto-detectar features categóricas vs numéricas correctamente
        self.true_numerical_features = []
        self.true_categorical_features = []
        
        # Features que son verdaderamente numéricas (sin guiones bajos de one-hot)
        true_numerical_names = [
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
        
        # Clasificar correctamente
        for feature in features:
            if feature in true_numerical_names:
                self.true_numerical_features.append(feature)
            else:
                # Todo lo demás son columnas one-hot encoded (categóricas)
                self.true_categorical_features.append(feature)
        
        # Mapear nombres de campo del API a nombres del dataset
        self.field_mapping = {
            'mothers_qualification': "mother's_qualification",
            'fathers_qualification': "father's_qualification"
        }
        
        print(f"🏗️ Pipeline inicializado con:")
        print(f"   Features totales: {len(self.features)}")
        print(f"   Numéricas REALES: {len(self.true_numerical_features)}")
        print(f"   Categóricas REALES (one-hot): {len(self.true_categorical_features)}")
    
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
        
        print(f"\n🔧 Procesando variables categóricas (one-hot encoding)...")
        
        # 2. Crear columnas one-hot a partir de valores categóricos originales
        for one_hot_feature in self.true_categorical_features:
            # Parsear el nombre de la feature one-hot
            # Ejemplo: "scholarship_holder_Yes" → base="scholarship_holder", expected_value="Yes"
            
            if '_' not in one_hot_feature:
                continue
                
            # Encontrar la separación correcta entre base y value
            parts = one_hot_feature.split('_')
            
            # Para features con múltiples palabras, tenemos que ser inteligentes
            if len(parts) >= 2:
                # Caso especial para mother's/father's qualification
                if one_hot_feature.startswith("mother's_qualification_"):
                    base_name = "mother's_qualification"
                    expected_value = one_hot_feature.replace("mother's_qualification_", "")
                elif one_hot_feature.startswith("father's_qualification_"):
                    base_name = "father's_qualification"
                    expected_value = one_hot_feature.replace("father's_qualification_", "")
                elif one_hot_feature.startswith("marital_status_"):
                    base_name = "marital_status"
                    expected_value = one_hot_feature.replace("marital_status_", "")
                elif one_hot_feature.startswith("scholarship_holder_"):
                    base_name = "scholarship_holder"
                    expected_value = one_hot_feature.replace("scholarship_holder_", "")
                elif one_hot_feature.startswith("tuition_fees_up_to_date_"):
                    base_name = "tuition_fees_up_to_date"
                    expected_value = one_hot_feature.replace("tuition_fees_up_to_date_", "")
                elif one_hot_feature.startswith("previous_qualification_"):
                    base_name = "previous_qualification"
                    expected_value = one_hot_feature.replace("previous_qualification_", "")
                else:
                    # Fallback: usar los primeros 2 elementos como base
                    base_name = "_".join(parts[:2])
                    expected_value = "_".join(parts[2:])
                
                # Buscar la columna original en el dataframe de entrada
                if base_name in X_processed.columns:
                    actual_value = str(X_processed[base_name].iloc[0])
                    
                    # Crear columna one-hot: 1 si coincide, 0 si no
                    X_processed[one_hot_feature] = 1 if actual_value == expected_value else 0
                    
                    if X_processed[one_hot_feature].iloc[0] == 1:
                        print(f"✅ {one_hot_feature} = 1 | '{actual_value}' == '{expected_value}' ✓")
                    else:
                        print(f"   {one_hot_feature} = 0 | '{actual_value}' != '{expected_value}'")
                else:
                    # Si no encontramos la columna base, poner 0
                    X_processed[one_hot_feature] = 0
                    print(f"❌ No encontrada columna base '{base_name}' para {one_hot_feature}")
        
        # 3. Eliminar columnas categóricas originales (que ya convertimos a one-hot)
        original_categorical_columns = [
            'scholarship_holder', 'tuition_fees_up_to_date', 'marital_status',
            'previous_qualification', "mother's_qualification", "father's_qualification"
        ]
        
        for col in original_categorical_columns:
            if col in X_processed.columns:
                X_processed.drop(col, axis=1, inplace=True)
                print(f"🗑️ Eliminada columna categórica original: {col}")
        
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
        for feat, val in list(non_zero_features.items())[:15]:  # Mostrar más ejemplos
            print(f"     {feat}: {val}")
        if len(non_zero_features) > 15:
            print(f"     ... y {len(non_zero_features) - 15} más")
        
        print(f"   Suma total: {result.sum().sum()}")
        
        return result
    
    def fit_transform(self, X, y=None):
        return self.transform(X)