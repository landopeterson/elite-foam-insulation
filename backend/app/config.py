"""App settings loaded from environment / .env. No secrets are hardcoded."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = ""
    supabase_service_role_key: str = ""

    # Email (Resend)
    resend_api_key: str = ""
    lead_notify_to: str = ""
    lead_notify_from: str = ""

    # CORS
    frontend_origin: str = "http://localhost:5173"

    # Look for .env at the project root (one level up from backend/).
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
