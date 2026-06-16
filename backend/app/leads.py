"""Lead persistence (Supabase) + owner notification (Resend email).

Both clients are created lazily so the app boots fine without credentials (e.g. in dev or
before the keys are filled in) — they only error when actually used.
"""
from __future__ import annotations

import logging

import httpx
from supabase import Client, create_client

from app.config import get_settings

logger = logging.getLogger("sprayfoam")
settings = get_settings()

_supabase: Client | None = None


def _client() -> Client:
    """Cached Supabase client using the service-role key (server-side; bypasses RLS)."""
    global _supabase
    if _supabase is None:
        _supabase = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _supabase


def save_lead(lead: dict) -> None:
    """Insert a lead row. Only known columns are sent."""
    row = {
        "name": lead.get("name"),
        "email": lead.get("email"),
        "phone": lead.get("phone"),
        "service": lead.get("service"),
        "message": lead.get("message"),
        "source": lead.get("source") or "website",
    }
    _client().table("leads").insert(row).execute()


def notify_owner(lead: dict) -> None:
    """Email the owner about a new lead via Resend. No-op if email isn't configured."""
    if not (settings.resend_api_key and settings.lead_notify_to and settings.lead_notify_from):
        logger.info("Email not configured — skipping owner notification.")
        return

    subject = f"New quote request from {lead.get('name', 'someone')}"
    lines = [
        f"Name:    {lead.get('name') or '—'}",
        f"Phone:   {lead.get('phone') or '—'}",
        f"Email:   {lead.get('email') or '—'}",
        f"Service: {lead.get('service') or '—'}",
        "",
        "Message:",
        lead.get("message") or "(none)",
    ]
    body = "\n".join(lines)

    resp = httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {settings.resend_api_key}"},
        json={
            "from": settings.lead_notify_from,
            "to": [settings.lead_notify_to],
            "subject": subject,
            "text": body,
            "reply_to": lead.get("email") or None,
        },
        timeout=10,
    )
    resp.raise_for_status()
