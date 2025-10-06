from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("SUPABASE_URL or SUPABASE_KEY not found in environment variables")

supabase = create_client(supabase_url, supabase_key)
