import sys
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
sys.path.append(os.path.abspath('.'))

from server.database.supabase_client import supabase
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def get_database_connection():
    """
    Obtiene la conexión directa a PostgreSQL usando las credenciales de tu .env
    """
    # Usar las variables específicas de PostgreSQL de tu .env
    postgres_host = os.environ.get("POSTGRES_HOST")
    postgres_db = os.environ.get("POSTGRES_DB") 
    postgres_user = os.environ.get("POSTGRES_USER")
    postgres_password = os.environ.get("POSTGRES_PASSWORD")
    postgres_port = os.environ.get("POSTGRES_PORT", "5432")
    
    # Verificar que todas las variables están presentes
    required_vars = {
        "POSTGRES_HOST": postgres_host,
        "POSTGRES_DB": postgres_db,
        "POSTGRES_USER": postgres_user, 
        "POSTGRES_PASSWORD": postgres_password
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    if missing_vars:
        print(f"❌ Variables faltantes en .env: {', '.join(missing_vars)}")
        return None
    
    print(f"🔗 Conectando a PostgreSQL:")
    print(f"   Host: {postgres_host}")
    print(f"   Database: {postgres_db}")
    print(f"   User: {postgres_user}")
    print(f"   Port: {postgres_port}")
    
    try:
        conn = psycopg2.connect(
            host=postgres_host,
            database=postgres_db,
            user=postgres_user,
            password=postgres_password,
            port=int(postgres_port),
            cursor_factory=RealDictCursor
        )
        
        print("✅ Conexión a PostgreSQL establecida")
        return conn
        
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        print("💡 Verifica las credenciales de PostgreSQL en tu .env")
        return None

def create_students_table_if_not_exists(conn):
    """
    Crea la tabla students completa si no existe
    """
    print("🏗️ Verificando/creando tabla students...")
    
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS students (
        id BIGSERIAL PRIMARY KEY,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        
        -- Campos académicos (basados en StudentInput schema)
        curricular_units_1st_sem_grade REAL NOT NULL,
        curricular_units_2nd_sem_grade REAL NOT NULL,
        curricular_units_1st_sem_approved INTEGER NOT NULL,
        curricular_units_2nd_sem_approved INTEGER NOT NULL,
        curricular_units_1st_sem_evaluations INTEGER NOT NULL,
        curricular_units_2nd_sem_evaluations INTEGER NOT NULL,
        unemployment_rate REAL NOT NULL,
        gdp REAL NOT NULL,
        age_at_enrollment INTEGER NOT NULL,
        
        -- Campos categóricos
        scholarship_holder TEXT NOT NULL,
        tuition_fees_up_to_date TEXT NOT NULL,
        marital_status TEXT NOT NULL,
        previous_qualification TEXT NOT NULL,
        mothers_qualification TEXT NOT NULL,
        fathers_qualification TEXT NOT NULL,
        
        -- Campo resultado
        target TEXT NOT NULL,
        
        -- Campos para predicciones ML (nuevos)
        probability_graduate REAL,
        probability_dropout REAL,
        probability_enrolled REAL,
        predicted_outcome TEXT,
        confidence REAL
    );
    """
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
            conn.commit()
            print("✅ Tabla students creada/verificada exitosamente")
            return True
    except Exception as e:
        print(f"❌ Error creando tabla: {e}")
        conn.rollback()
        return False

def add_missing_ml_columns(conn):
    """
    Agrega las columnas ML si no existen (para tablas existentes)
    """
    print("🔧 Verificando/agregando columnas ML...")
    
    ml_columns = [
        ('probability_graduate', 'REAL'),
        ('probability_dropout', 'REAL'), 
        ('probability_enrolled', 'REAL'),
        ('predicted_outcome', 'TEXT'),
        ('confidence', 'REAL')
    ]
    
    added_columns = []
    
    try:
        with conn.cursor() as cursor:
            for column_name, column_type in ml_columns:
                # Verificar si la columna existe
                cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'students' AND column_name = %s
                """, (column_name,))
                
                if not cursor.fetchone():
                    # La columna no existe, agregarla
                    alter_sql = f"ALTER TABLE students ADD COLUMN {column_name} {column_type};"
                    cursor.execute(alter_sql)
                    added_columns.append(column_name)
                    print(f"   ✅ Agregada columna: {column_name}")
                else:
                    print(f"   ✓ Columna ya existe: {column_name}")
            
            conn.commit()
            
            if added_columns:
                print(f"📊 Se agregaron {len(added_columns)} columnas ML")
            else:
                print("📊 Todas las columnas ML ya existían")
                
            return True
            
    except Exception as e:
        print(f"❌ Error agregando columnas ML: {e}")
        conn.rollback()
        return False

def verify_table_schema(conn):
    """
    Verifica el esquema final de la tabla
    """
    print("🔍 Verificando esquema final...")
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'students'
                ORDER BY ordinal_position
            """)
            
            columns = cursor.fetchall()
            
            print(f"✅ Tabla students configurada con {len(columns)} columnas:")
            
            ml_columns = ['probability_graduate', 'probability_dropout', 'probability_enrolled', 'predicted_outcome', 'confidence']
            found_ml = []
            
            for col in columns:
                col_name = col['column_name']
                if col_name in ml_columns:
                    found_ml.append(col_name)
                    print(f"   🤖 {col_name} ({col['data_type']})")
                elif col_name not in ['id', 'created_at']:
                    print(f"   📋 {col_name} ({col['data_type']})")
            
            missing_ml = set(ml_columns) - set(found_ml)
            if missing_ml:
                print(f"⚠️ Columnas ML faltantes: {list(missing_ml)}")
                return False
            else:
                print("✅ Todas las columnas ML están presentes")
                return True
                
    except Exception as e:
        print(f"❌ Error verificando esquema: {e}")
        return False

def clear_existing_data():
    """
    Limpia datos existentes usando Supabase client
    """
    print("🗑️ Limpiando datos existentes...")
    
    try:
        count_response = supabase.table("students").select("id", count="exact").execute()
        current_count = count_response.count if count_response.count else 0
        
        if current_count == 0:
            print("✅ La tabla ya está vacía")
            return True
        
        print(f"📊 Encontrados {current_count} registros existentes")
        confirm = input("¿Eliminar todos los datos existentes? (s/n): ")
        
        if confirm.lower() not in ['s', 'si', 'y', 'yes']:
            print("❌ Operación cancelada")
            return False
        
        response = supabase.table("students").delete().gte("id", 0).execute()
        print(f"✅ Eliminados {current_count} registros")
        return True
        
    except Exception as e:
        print(f"❌ Error limpiando datos: {e}")
        return False

def create_sample_data():
    """
    Crea datos de ejemplo usando Supabase client
    """
    print("📊 Creando datos de ejemplo...")
    
    sample_students = [
        {
            # Estudiante exitoso
            'curricular_units_1st_sem_grade': 18.5,
            'curricular_units_2nd_sem_grade': 19.0,
            'curricular_units_1st_sem_approved': 6,
            'curricular_units_2nd_sem_approved': 6,
            'curricular_units_1st_sem_evaluations': 6,
            'curricular_units_2nd_sem_evaluations': 6,
            'unemployment_rate': 7.0,
            'gdp': 2.5,
            'age_at_enrollment': 19,
            'scholarship_holder': 'Yes',
            'tuition_fees_up_to_date': 'Yes',
            'marital_status': 'Single',
            'previous_qualification': 'Secondary education',
            'mothers_qualification': 'Higher education—bachelor\'s degree',
            'fathers_qualification': 'Higher education—degree',
            'target': 'Graduate',
            'probability_graduate': 0.87,
            'probability_dropout': 0.08,
            'probability_enrolled': 0.05,
            'predicted_outcome': 'Graduate',
            'confidence': 0.87
        },
        {
            # Estudiante en riesgo
            'curricular_units_1st_sem_grade': 8.0,
            'curricular_units_2nd_sem_grade': 7.5,
            'curricular_units_1st_sem_approved': 2,
            'curricular_units_2nd_sem_approved': 1,
            'curricular_units_1st_sem_evaluations': 8,
            'curricular_units_2nd_sem_evaluations': 9,
            'unemployment_rate': 15.0,
            'gdp': -0.5,
            'age_at_enrollment': 35,
            'scholarship_holder': 'No',
            'tuition_fees_up_to_date': 'No',
            'marital_status': 'Divorced',
            'previous_qualification': 'Basic education 3rd cycle (9th/10th/11th year) or equivalent',
            'mothers_qualification': 'Cannot read or write',
            'fathers_qualification': 'Unknown',
            'target': 'Dropout',
            'probability_graduate': 0.18,
            'probability_dropout': 0.68,
            'probability_enrolled': 0.14,
            'predicted_outcome': 'Dropout',
            'confidence': 0.68
        },
        {
            # Estudiante promedio
            'curricular_units_1st_sem_grade': 13.0,
            'curricular_units_2nd_sem_grade': 12.5,
            'curricular_units_1st_sem_approved': 4,
            'curricular_units_2nd_sem_approved': 3,
            'curricular_units_1st_sem_evaluations': 6,
            'curricular_units_2nd_sem_evaluations': 7,
            'unemployment_rate': 11.0,
            'gdp': 1.0,
            'age_at_enrollment': 22,
            'scholarship_holder': 'Yes',
            'tuition_fees_up_to_date': 'Yes',
            'marital_status': 'Single',
            'previous_qualification': 'Secondary education',
            'mothers_qualification': 'Secondary education—12th year of schooling or equivalent',
            'fathers_qualification': 'Secondary education—12th year of schooling or equivalent',
            'target': 'Enrolled',
            'probability_graduate': 0.35,
            'probability_dropout': 0.25,
            'probability_enrolled': 0.40,
            'predicted_outcome': 'Enrolled',
            'confidence': 0.40
        }
    ]
    
    success_count = 0
    student_types = ["exitoso 🎓", "en riesgo ⚠️", "promedio 📊"]
    
    for i, student in enumerate(sample_students):
        try:
            response = supabase.table("students").insert(student).execute()
            if response.data:
                success_count += 1
                print(f"   ✅ Estudiante {student_types[i]} creado (ID: {response.data[0]['id']})")
        except Exception as e:
            print(f"   ❌ Error con estudiante {student_types[i]}: {e}")
    
    print(f"📈 {success_count}/{len(sample_students)} estudiantes creados exitosamente")
    return success_count > 0

def initialize_complete_database():
    """
    Inicialización completa de la base de datos
    """
    print("🚀 INICIALIZACIÓN COMPLETA DE BASE DE DATOS")
    print("=" * 55)
    print("Configurando tabla 'students' desde cero para tu proyecto")
    print("=" * 55)
    
    # Paso 1: Conectar a PostgreSQL directamente usando tu configuración
    conn = get_database_connection()
    if not conn:
        print("\n💡 PROBLEMA DE CONFIGURACIÓN:")
        print("Verifica que estas variables estén en tu .env:")
        print("   POSTGRES_HOST=aws-0-us-east-2.pooler.supabase.com")
        print("   POSTGRES_DB=postgres")
        print("   POSTGRES_USER=postgres.pajghemlgekomqscqeme")
        print("   POSTGRES_PASSWORD=proyectogrupo3.")
        print("   POSTGRES_PORT=5432")
        return False
    
    try:
        # Paso 2: Crear tabla completa
        if not create_students_table_if_not_exists(conn):
            return False
        
        # Paso 3: Agregar columnas ML si faltan
        if not add_missing_ml_columns(conn):
            return False
        
        # Paso 4: Verificar esquema final
        if not verify_table_schema(conn):
            return False
        
    finally:
        conn.close()
        print("🔌 Conexión PostgreSQL cerrada")
    
    # Paso 5: Limpiar datos existentes (usando Supabase client)
    if not clear_existing_data():
        return False
    
    # Paso 6: Crear datos de ejemplo
    create_examples = input("\n¿Crear datos de ejemplo? (s/n): ").lower() in ['s', 'si', 'y', 'yes']
    
    if create_examples:
        if not create_sample_data():
            print("⚠️ Error creando datos de ejemplo, pero la tabla está lista")
    
    # Resumen final
    print("\n" + "=" * 55)
    print("🎉 ¡INICIALIZACIÓN COMPLETADA!")
    print("=" * 55)
    print("✅ Tabla 'students' configurada completamente")
    print("🤖 Columnas ML listas para predicciones")
    print("📊 Sistema listo para tu API FastAPI + XGBoost")
    
    print("\n🔗 Tu sistema está listo:")
    print("   • API Predicciones: http://localhost:8000/predict")
    print("   • Ver estudiantes: http://localhost:8000/students") 
    print("   • Estado modelo: http://localhost:8000/model/status")
    print("   • Dashboard React: http://localhost:3000/monitoring")
    
    print("\n📋 Archivos importantes:")
    print("   • Esquema: server/models/schemas.py")
    print("   • API: server/main.py")
    print("   • Modelo: server/models/predictor.py")
    
    return True

if __name__ == "__main__":
    # Verificar dependencias
    try:
        import psycopg2
    except ImportError:
        print("❌ psycopg2 no está instalado")
        print("📦 Instala con: pip install psycopg2-binary")
        sys.exit(1)
    
    success = initialize_complete_database()
    
    if success:
        print("\n🎯 ¡Tu proyecto está listo para ser clonado por otros desarrolladores!")
        print("💡 Solo necesitan configurar su .env con sus credenciales de Supabase")
    else:
        print("\n❌ Configuración incompleta. Revisa los errores anteriores.")
        print("💡 Asegúrate de tener DATABASE_URL en tu .env")