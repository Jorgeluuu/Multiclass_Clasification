# server/models/preprocessing.py
import pandas as pd
import os

class PreprocessingPipeline:
    def __init__(self, features, categorical_features=None, numerical_features=None):
        self.features = features
        self.categorical_features = categorical_features or []
        self.numerical_features = numerical_features or []
        self.categorical_bases = []
        
        for feature in self.categorical_features:
            base = feature.split('_')[0]
            if base not in self.categorical_bases:
                self.categorical_bases.append(base)
    
    def transform(self, X):
        X_processed = X.copy()
        
        for base_feature in self.categorical_bases:
            if base_feature in X_processed.columns:
                value = X_processed[base_feature].iloc[0]
                
                for cat_feature in self.categorical_features:
                    if cat_feature.startswith(base_feature + '_'):
                        feature_value = cat_feature.split('_', 1)[1]
                        X_processed[cat_feature] = 1 if str(value) == feature_value else 0
                
                X_processed = X_processed.drop(base_feature, axis=1)
        
        missing_features = set(self.features) - set(X_processed.columns)
        for feature in missing_features:
            X_processed[feature] = 0
        
        return X_processed[self.features]
    
    def fit_transform(self, X, y=None):
        return self.transform(X)