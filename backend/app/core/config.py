# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str

    # CocktailDB
    COCKTAILDB_BASE: str = "https://www.thecocktaildb.com/api/json/v1"
    COCKTAILDB_KEY: str = "1"

    # App
    APP_ENV: str = "dev"
    APP_PORT: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()