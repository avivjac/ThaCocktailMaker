# app/main.py
from fastapi import FastAPI
from app.API import pantry as pantry_routes

app = FastAPI(title="HomeBar API")

app.include_router(pantry_routes.router)

# בריאות
@app.get("/health")
def health():
    return {"ok": True}
