# SprayFoam Site

Marketing website + contact form for a spray foam insulation business. The site brings in
leads; a contact form captures them, stores them in Supabase, and emails the owner.

This is a **hybrid build**: a static, fast marketing site (great for local SEO) plus a thin
FastAPI + Supabase layer that owns the contact form and lead storage. A dedicated scheduler
(Cal.com) is intentionally deferred — start with a simple contact form.

## Stack

- **Frontend:** marketing site (hero, services, about, contact). Built for local SEO + mobile.
- **Backend:** FastAPI (Python) — `/contact` endpoint: validates a submission, stores the lead,
  emails the owner. Holds all secrets.
- **Database:** Supabase (Postgres) — a single `leads` table.
- **Hosting (planned):** frontend on Vercel/Netlify (free), backend on a free tier, Supabase free tier.

## Project layout

```
backend/    FastAPI app (contact endpoint, config)
frontend/   Marketing site (added in Phase 3)
supabase/   SQL schema for the leads table
```

## Build phases

- [x] **Phase 0** — Project skeleton.
- [ ] **Phase 1** — Supabase `leads` table + insert policy.
- [ ] **Phase 2** — FastAPI `/contact` endpoint (store lead + email owner).
- [ ] **Phase 3** — Frontend marketing site + contact form.
- [ ] **Phase 4** — Deploy + custom domain.
- [ ] *Later* — Owner admin page (self-edit content); Cal.com scheduler.

## Business details (fill in)

These drive the site content. TBD until provided:

- **Business name:** TBD
- **Owner phone / email (lead destination):** TBD
- **Service area:** TBD
- **Services:** TBD (e.g. open-cell / closed-cell foam, attics, crawlspaces, new construction, commercial)
- **Logo / photos:** TBD
- **Brand vibe:** TBD

## Local setup

### Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env   # then fill in real values
uvicorn app.main:app --reload --port 8000
```
Visit http://localhost:8000/health to confirm it's running.
