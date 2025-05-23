import os
from supabase import create_client, Client, ClientOptions
from dotenv import load_dotenv
from httpx import Client as HTTPXClient
# Cargar variables de entorno exactas a que apunten a un sitio o puede haber problemas al ejecutar uvicorn
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")

# Hay muchos errores con la librería httpx con supabase ya que está intentando encontrar un certificado SSL y cada vez se está desactivando desde terminal, para evitarlo, se añade esta línea
# Esto desactiva la verificación SSL
os.environ.pop("SSL_CERT_FILE", None)
client_options = ClientOptions(headers={"Authorization": f"Bearer {supabase_key}"})

supabase: Client = create_client(supabase_url, supabase_key, options=client_options)


print("✅ Cliente de Supabase inicializado.")

# ---------------------------------
# _supabase: Client = None

# def get_supabase_client() -> Client:
#     global _supabase
#     if _supabase is None:
#         os.environ.pop("SSL_CERT_FILE", None)  # Evitar errores de certificado
#         client_options = ClientOptions(headers={"Authorization": f"Bearer {supabase_key}"})
#         _supabase = create_client(supabase_url, supabase_key, options=client_options)
#         print("✅ Cliente de Supabase inicializado.")
#     return _supabase

# import logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
# logger.info("✅ Cliente de Supabase inicializado.")
