"""FastAPI entrypoint for the SprayFoam site backend.

Phase 0: scaffolding + health check only. The /contact endpoint arrives in Phase 2.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings

settings = get_settings()

app = FastAPI(title="SprayFoam Site API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Liveness check + which integrations are configured (booleans only, no secrets)."""
    return {
        "status": "ok",
        "configured": {
            "supabase": bool(settings.supabase_url and settings.supabase_service_role_key),
            "email": bool(settings.resend_api_key and settings.lead_notify_to),
        },
    }
