# app/db/supabase.py
from __future__ import annotations
from typing import Any, Dict, List, Optional, Iterable
import httpx
from supabase import create_client, Client
from app.core.config import settings


# ========= Exceptions =========

class DBError(Exception):
    """General database error wrapper."""
    pass

class AuthError(Exception):
    """JWT missing/invalid/expired."""
    pass


# ========= Clients =========

def get_user_client(user_jwt: str) -> Client:
    """
    יוצר קליינט תחת זהות משתמש לצורך RLS.
    מצפה ל-JWT חוקי שקיבלת מהפרונט (Supabase Auth).
    """
    if not user_jwt:
        raise AuthError("Missing user JWT")
    sb = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    sb.postgrest.auth(user_jwt)
    return sb

def get_service_client() -> Client:
    """
    קליינט עם Service Role - עוקף RLS. להשתמש רק בצד שרת מאובטח.
    """
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)


# ========= Auth helpers =========

async def get_user_from_jwt(user_jwt: str) -> Dict[str, Any]:
    """
    מאמת JWT ומחזיר פרטי משתמש מ-Supabase Auth (דרך REST).
    לא דורש ספריית JWT — Supabase מאמת עבורנו.
    """
    if not user_jwt:
        raise AuthError("Missing user JWT")

    url = f"{settings.SUPABASE_URL}/auth/v1/user"
    headers = {
        "Authorization": f"Bearer {user_jwt}",
        "apikey": settings.SUPABASE_ANON_KEY,
    }
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, headers=headers)
        if r.status_code != 200:
            raise AuthError(f"Invalid/expired user token (status={r.status_code})")
        return r.json()

async def get_user_id_from_jwt(user_jwt: str) -> str:
    user = await get_user_from_jwt(user_jwt)
    user_id = user.get("id") or user.get("user", {}).get("id")
    if not user_id:
        raise AuthError("Could not resolve user_id from token")
    return user_id


# ========= Pantry =========

async def get_user_pantry(user_jwt: str) -> List[Dict[str, Any]]:
    """
    מחזיר את הפאנטרי של המשתמש המחובר.
    """
    sb = get_user_client(user_jwt)
    try:
        resp = sb.table("user_pantry") \
                 .select("id, ingredient_id, custom_name, has, amount_ml") \
                 .order("id") \
                 .execute()
        return resp.data or []
    except Exception as e:
        raise DBError(f"Failed to fetch user pantry: {e}") from e


async def upsert_user_pantry(
    user_jwt: str,
    items: Iterable[Dict[str, Any]]
) -> int:
    """
    Upsert לרשימת פריטים בפאנטרי.
    items דוגמה:
      [{"ingredient_id": 1, "has": True, "amount_ml": 700},
       {"custom_name": "Monin Passionfruit", "has": True}]
    """
    user_id = await get_user_id_from_jwt(user_jwt)
    sb = get_user_client(user_jwt)

    rows = []
    for it in items:
        rows.append({
            "user_id": user_id,
            "ingredient_id": it.get("ingredient_id"),
            "custom_name": it.get("custom_name"),
            "has": it.get("has", True),
            "amount_ml": it.get("amount_ml"),
        })

    try:
        # חשוב: on_conflict לפי (user_id, ingredient_id)
        resp = sb.table("user_pantry") \
                 .upsert(rows, on_conflict="user_id,ingredient_id") \
                 .execute()
        return len(resp.data or [])
    except Exception as e:
        raise DBError(f"Failed to upsert pantry: {e}") from e


async def delete_user_pantry_item(
    user_jwt: str,
    ingredient_id: Optional[int] = None,
    custom_name: Optional[str] = None
) -> int:
    """
    מוחק רשומה אחת מהפאנטרי לפי ingredient_id או custom_name.
    """
    if not ingredient_id and not custom_name:
        raise ValueError("Provide ingredient_id or custom_name")

    sb = get_user_client(user_jwt)
    try:
        q = sb.table("user_pantry")
        if ingredient_id:
            q = q.eq("ingredient_id", ingredient_id)
        if custom_name:
            q = q.eq("custom_name", custom_name)
        resp = q.delete().execute()
        # חלק מהגרסאות לא מחזירות data במחיקה; נחזיר 1 אם לא נזרקה שגיאה
        return len(resp.data or []) if hasattr(resp, "data") else 1
    except Exception as e:
        raise DBError(f"Failed to delete pantry item: {e}") from e


# ========= Ratings =========

# async def upsert_rating(
#     user_jwt: str,
#     cocktail_id: str,
#     stars: Optional[int] = None,
#     liked: Optional[bool] = None,
#     notes: Optional[str] = None
# ) -> None:
#     user_id = await get_user_id_from_jwt(user_jwt)
#     sb = get_user_client(user_jwt)
#     try:
#         sb.table("ratings").upsert({
#             "user_id": user_id,
#             "cocktail_id": cocktail_id,
#             "stars": stars,
#             "liked": liked,
#             "notes": notes
#         }, on_conflict="user_id,cocktail_id").execute()
#     except Exception as e:
#         raise DBError(f"Failed to upsert rating: {e}") from e


# async def get_ratings(user_jwt: str) -> List[Dict[str, Any]]:
#     sb = get_user_client(user_jwt)
#     try:
#         resp = sb.table("ratings") \
#                  .select("cocktail_id, stars, liked, notes, created_at") \
#                  .order("created_at", desc=True) \
#                  .execute()
#         return resp.data or []
#     except Exception as e:
#         raise DBError(f"Failed to fetch ratings: {e}") from e


# ========= Profiles helper =========

async def ensure_profile(user_jwt: str, username: Optional[str] = None) -> None:
    """
    מבטיח קיום רשומת פרופיל תואמת ל-auth.users (לפי user_id).
    """
    user_id = await get_user_id_from_jwt(user_jwt)
    sb = get_user_client(user_jwt)
    try:
        sb.table("profiles").upsert({
            "id": user_id,
            "username": username
        }).execute()
    except Exception as e:
        raise DBError(f"Failed to ensure profile: {e}") from e


# ========= Ingredients seeding (Service role only) =========

# async def seed_ingredients_service(rows: Iterable[Dict[str, Any]]) -> int:
#     """
#     הכנסת/עדכון רשומות ל-ingredients עם Service Role. rows דוגמה:
#       [{"name":"Vodka","type":"spirit","abv":40,"flavor_tags":["neutral"]}, ...]
#     """
#     sb = get_service_client()
#     try:
#         resp = sb.table("ingredients").upsert(list(rows), on_conflict="name").execute()
#         return len(resp.data or [])
#     except Exception as e:
#         raise DBError(f"Failed to seed ingredients: {e}") from e
