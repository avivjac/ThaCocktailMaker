# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.API import pantry as pantry_routes

app = FastAPI(title="HomeBar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pantry_routes.router)

# בריאות
@app.get("/health")
def health():
    return {"ok": True}
