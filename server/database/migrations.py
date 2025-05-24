import sys
import os
sys.path.append(os.path.abspath('.'))

from server.database.supabase_client import supabase
from datetime import datetime

class DatabaseMigration:
    """
    Sistema de migración para crear y mantener la estructura de la base de datos
    """
    
    def __init__(self):
        self.table_name = "students"
        
    def get_complete_student_schema(self):
        """
        Define el esquema completo de la tabla students con TODAS las columnas necesarias
        """
        return {
            # ✅ CAMPOS PRINCIPALES DEL ESTUDIANTE
            'curricular_units_1st_sem_grade': 15.0,      # REAL
            'curricular_units_2nd_sem_grade': 14.5,      # REAL  
            'curricular_units_1st_sem_approved': 5,      # INTEGER
            'curricular_units_2nd_sem_approved': 4,      # INTEGER
            'curricular_units_1st_sem_evaluations': 6,   # INTEGER
            'curricular_units_2nd_sem_evaluations': 5,   # INTEGER
            'unemployment_rate': 10.0,                   # REAL
            'gdp': 1.5,                                  # REAL
            'age_at_enrollment': 20,                     # INTEGER
            
            # ✅ CAMPOS CATEGÓRICOS
            'scholarship_holder': 'Yes',                 # TEXT
            'tuition_fees_up_to_date': 'Yes',           # TEXT
            'marital_status': 'Single',                 # TEXT
            'previous_qualification': 'Secondary education',  # TEXT
            'mothers_qualification': 'Higher education—bachelor\'s degree',  # TEXT
            'fathers_qualification': 'Secondary education—12th year of schooling or equivalent',  # TEXT
            
            # ✅ RESULTADO REAL (TARGET)
            'target': 'Graduate',                       # TEXT
            
            # ✅ PROBABILIDADES DEL MODELO ML (NUEVAS COLUMNAS)
            'probability_graduate': 0.75,              # REAL
            'probability_dropout': 0.15,               # REAL
            'probability_enrolled': 0.10,              # REAL
            
            # ✅ METADATA DE LA PREDICCIÓN
            'predicted_outcome': 'Graduate',           # TEXT - Clase predicha por el modelo
            'confidence': 0.75,                        # REAL - Confianza (probabilidad máxima)
            
            # ✅ CAMPOS AUTOMÁTICOS (Supabase los maneja)
            # 'id': AUTO_INCREMENT PRIMARY KEY
            # 'created_at': TIMESTAMP DEFAULT NOW()
            # 'updated_at': TIMESTAMP DEFAULT NOW()
        }
    
    def create_table_with_schema(self):
        """
        Crea la tabla con el esquema completo insertando un registro que define todas las columnas
        """
        print("🏗️ Creando tabla students con esquema completo...")
        
        # Obtener datos de ejemplo con todas las columnas
        complete_schema = self.get_complete_student_schema()
        
        try:
            print("📋 Esquema definido:")
            print("   Campos numéricos:", len([k for k, v in complete_schema.items() if isinstance(v, (int, float))]))
            print("   Campos de texto:", len([k for k, v in complete_schema.items() if isinstance(v, str)]))
            print("   Total columnas:", len(complete_schema))
            
            # Insertar registro que crea todas las columnas
            print("\n🔨 Insertando registro de esquema...")
            response = supabase.table(self.table_name).insert(complete_schema).execute()
            
            if response.data:
                schema_record_id = response.data[0]['id']
                print(f"✅ Tabla creada con ID de esquema: {schema_record_id}")
                
                # Verificar que todas las columnas existen
                verify_response = supabase.table(self.table_name).select("*").limit(1).execute()
                if verify_response.data:
                    actual_columns = list(verify_response.data[0].keys())
                    print(f"✅ Columnas creadas exitosamente: {len(actual_columns)}")
                    
                    # Verificar columnas críticas
                    critical_columns = ['probability_graduate', 'probability_dropout', 'probability_enrolled', 'predicted_outcome', 'confidence']
                    missing_critical = [col for col in critical_columns if col not in actual_columns]
                    
                    if missing_critical:
                        print(f"⚠️ Columnas críticas faltantes: {missing_critical}")
                    else:
                        print("✅ Todas las columnas críticas presentes")
                
                return schema_record_id
            else:
                print("❌ Error: No se pudo crear el registro de esquema")
                return None
                
        except Exception as e:
            print(f"❌ Error creando tabla: {e}")
            return None
    
    def verify_schema(self):
        """
        Verifica que la tabla tiene todas las columnas necesarias
        """
        print("🔍 Verificando esquema de la tabla...")
        
        try:
            response = supabase.table(self.table_name).select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                actual_columns = list(response.data[0].keys())
                expected_columns = list(self.get_complete_student_schema().keys())
                
                print(f"📊 Columnas actuales: {len(actual_columns)}")
                print(f"📊 Columnas esperadas: {len(expected_columns)}")
                
                missing_columns = [col for col in expected_columns if col not in actual_columns]
                extra_columns = [col for col in actual_columns if col not in expected_columns and col not in ['id', 'created_at', 'updated_at']]
                
                if missing_columns:
                    print(f"❌ Columnas faltantes: {missing_columns}")
                    return False
                
                if extra_columns:
                    print(f"ℹ️ Columnas adicionales: {extra_columns}")
                
                print("✅ Esquema verificado correctamente")
                return True
            else:
                print("⚠️ Tabla vacía, no se puede verificar esquema")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando esquema: {e}")
            return False
    
    def populate_sample_data(self):
        """
        Prueba la tabla con datos de ejemplo para testing
        """
        print("📊 Poblando tabla con datos de ejemplo...")
        
        sample_students = [
            # Estudiante exitoso
            {
                'curricular_units_1st_sem_grade': 18.0,
                'curricular_units_2nd_sem_grade': 17.5,
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
                'fathers_qualification': 'Higher education—degree',
                'target': 'Graduate',
                'probability_graduate': 0.85,
                'probability_dropout': 0.10,
                'probability_enrolled': 0.05,
                'predicted_outcome': 'Graduate',
                'confidence': 0.85
            },
            # Estudiante en riesgo
            {
                'curricular_units_1st_sem_grade': 9.0,
                'curricular_units_2nd_sem_grade': 8.5,
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
                'fathers_qualification': 'Unknown',
                'target': 'Dropout',
                'probability_graduate': 0.15,
                'probability_dropout': 0.70,
                'probability_enrolled': 0.15,
                'predicted_outcome': 'Dropout',
                'confidence': 0.70
            }
        ]
        
        try:
            for i, student in enumerate(sample_students, 1):
                response = supabase.table(self.table_name).insert(student).execute()
                if response.data:
                    print(f"✅ Estudiante de ejemplo {i} insertado: ID {response.data[0]['id']}")
                else:
                    print(f"❌ Error insertando estudiante {i}")
            
            print(f"✅ {len(sample_students)} estudiantes de ejemplo agregados")
            return True
            
        except Exception as e:
            print(f"❌ Error poblando datos: {e}")
            return False
    
    def run_full_migration(self, include_sample_data=True):
        """
        Ejecuta la migración completa
        """
        print("🚀 INICIANDO MIGRACIÓN COMPLETA DE BASE DE DATOS")
        print("=" * 60)
        
        # Paso 1: Crear tabla con esquema completo
        schema_id = self.create_table_with_schema()
        if not schema_id:
            print("❌ Falló la creación del esquema")
            return False
        
        # Paso 2: Verificar esquema
        if not self.verify_schema():
            print("❌ Falló la verificación del esquema")
            return False
        
        # Paso 3: Poblar con datos de ejemplo (opcional)
        if include_sample_data:
            if not self.populate_sample_data():
                print("⚠️ Falló la inserción de datos de ejemplo (no crítico)")
        
        print("\n" + "=" * 60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print("🎯 La tabla students está lista para usar")
        print("🔗 Puedes probar el API ahora: http://localhost:8000/predict")
        print("📋 Ver datos: http://localhost:8000/students")
        
        return True

def main():
    """
    Función principal para ejecutar la migración
    """
    print("🔧 SISTEMA DE MIGRACIÓN DE BASE DE DATOS")
    print("📅", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("-" * 40)
    
    migration = DatabaseMigration()
    
    # Preguntar si incluir datos de ejemplo
    include_samples = input("¿Incluir datos de ejemplo? (s/n): ").lower() in ['s', 'si', 'y', 'yes']
    
    success = migration.run_full_migration(include_sample_data=include_samples)
    
    if success:
        print("\n🎉 ¡Base de datos lista para usar!")
    else:
        print("\n💥 Error en la migración")

if __name__ == "__main__":
    main()