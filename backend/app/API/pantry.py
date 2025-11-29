# app/api/routes/pantry.py
from fastapi import APIRouter, Depends, Header, HTTPException
from typing import Optional, List, Dict, Any
from app.DB.supabase import get_user_client

router = APIRouter(prefix="/pantry", tags=["pantry"])

def get_user_jwt(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization Bearer token")
    return authorization.split(" ", 1)[1]

@router.get("")
async def get_pantry(user_jwt: str = Depends(get_user_jwt)) -> Dict[str, Any]:
    try:
      pantry = await db.get_user_pantry(user_jwt)
      return {"pantry": pantry}
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))
    # sb = get_user_client(user_jwt)
    # resp = sb.table("user_pantry").select("id, ingredient_id, custom_name, has, amount_ml").execute()
    # return {"pantry": resp.data or []}

@router.put("")
def upsert_pantry(
    items: List[Dict[str, Any]],
    user_jwt: str = Depends(get_user_jwt)
) -> Dict[str, Any]:
    """
    body example:
    [
      {"ingredient_id": 1, "has": true, "amount_ml": 700},
      {"custom_name": "Monin Passionfruit", "has": true}
    ]
    """
    sb = get_user_client(user_jwt)

    # נזהה את המשתמש (באמצעות ה-JWT שסופאנייס מאפשר)
    # ספריית supabase-py v2 כוללת supabase.auth.get_user(token) ב־auth-helpers,
    # אם לא קיים בגרסתך, אפשר לפענח JWT מקומית או לקרוא ל-/auth/v1/user.
    # כאן נשתמש בפתרון פשוט דרך RPC של Supabase (טבלה virtual "auth.uid()"):
    # טריק: ננסה להכניס בלי user_id אם יש default? עדיף לא. נביא user_id בפועל:
    # פתרון פרקטי: קריאה ל-endpoint של auth כדי להביא את ה-user:
    try:
        auth_user = sb.auth.get_user(user_jwt)  # אם נתמך בגרסתך
        user_id = auth_user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid user token")

    rows = []
    for it in items:
        rows.append({
            "user_id": user_id,
            "ingredient_id": it.get("ingredient_id"),
            "custom_name": it.get("custom_name"),
            "has": it.get("has", True),
            "amount_ml": it.get("amount_ml"),
        })

    # חשוב: on_conflict לפי (user_id, ingredient_id)
    resp = sb.table("user_pantry").upsert(rows, on_conflict="user_id,ingredient_id").execute()
    return {"ok": True, "affected": len(resp.data or [])}
