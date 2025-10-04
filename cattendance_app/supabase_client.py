from supabase import create_client, Client
from django.conf import settings
# Helper function to create and return a Supabase client instance
def get_supabase_client():
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)