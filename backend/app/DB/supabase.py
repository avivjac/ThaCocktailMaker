# app/db/supabase.py
from supabase import create_client, Client
from app.core.config import settings

def get_user_client(user_jwt: str) -> Client:
    """
    יוצר קליינט תחת זהות משתמש לצורך RLS.
    מצפה ל-JWT חוקי שקיבלת מהפרונט (Supabase Auth).
    """
    sb = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    if user_jwt:
        sb.postgrest.auth(user_jwt)
    return sb

def get_service_client() -> Client:
    """
    קליינט עם Service Role - עוקף RLS. להשתמש רק בצד שרת מאובטח.
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
