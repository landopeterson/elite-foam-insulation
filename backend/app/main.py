"""FastAPI entrypoint for the Elite Foam Insulation site backend.

Endpoints:
  GET  /health   — liveness + which integrations are configured.
  POST /contact  — validate a contact-form submission, store it in Supabase, email the owner.
"""
import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, field_validator

from app.config import get_settings
from app.leads import save_lead, notify_owner

logger = logging.getLogger("sprayfoam")
settings = get_settings()

app = FastAPI(title="Elite Foam Insulation API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ContactIn(BaseModel):
    """A contact-form submission. Name is required; at least one of phone/email must be present."""
    name: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    service: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = "website"

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("Name is required.")
        return v

    @field_validator("phone", "service", "message", "source")
    @classmethod
    def strip_optional(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if isinstance(v, str) else v


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


@app.post("/contact")
def contact(payload: ContactIn) -> dict:
    """Store the lead, then try to email the owner. Storing is the source of truth;
    an email failure is logged but does not fail the request (the lead is safe in the DB)."""
    if not (payload.phone or payload.email):
        raise HTTPException(status_code=422, detail="Please provide a phone number or an email.")

    if not (settings.supabase_url and settings.supabase_service_role_key):
        # Don't pretend success — a dropped lead is worse than a visible error.
        raise HTTPException(status_code=503, detail="Lead storage is not configured yet.")

    lead = payload.model_dump()
    try:
        save_lead(lead)
    except Exception:
        logger.exception("Failed to store lead")
        raise HTTPException(status_code=502, detail="Could not save your request. Please call us.")

    # Best-effort notification — the lead is already saved, so never fail the request on email.
    try:
        notify_owner(lead)
    except Exception:
        logger.exception("Lead saved but owner notification failed")

    return {"ok": True}
