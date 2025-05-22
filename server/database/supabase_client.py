import os
from supabase import create_client, Client
from dotenv import load_dotenv
import os
# # Cargar variables de entorno
# load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")


supabase: Client = create_client(supabase_url, supabase_key)

print("✅ Cliente de Supabase inicializado.")