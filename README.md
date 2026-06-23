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
- [x] **Phase 1** — Supabase `leads` table + RLS (public INSERT only; reads locked to the secret key).
- [x] **Phase 2** — Lead capture: form posts directly to Supabase (publishable key).
- [x] **Phase 3** — Marketing site (real logo, photos, foam-cursor hero, contact form).
- [x] **Phase 4** — Deployed to Vercel (GitHub auto-deploy) + domain on Cloudflare.
- [x] **Email alerts** — Supabase webhook → Vercel `/api/notify` → Resend → owner inbox.

## TO DO (next session)

- [ ] **Add Cloudflare Turnstile (free captcha) to the contact form.** Spam bots can submit through
  the open insert policy (an SEO-pitch spam lead already came through). Add the Turnstile widget to
  the form and verify the token before/at insert (e.g. move inserts behind a Vercel function that
  checks the token, or validate in the webhook). Goal: block bots without bugging real visitors.
- [ ] **Google Workspace** mailboxes for Grant + partner at `@elitesprayinsulation.com`, then point
  the website's lead alerts (`LEAD_NOTIFY_TO` env var in Vercel) to the new address.
- [ ] *Later* — owner admin page (self-edit content); Cal.com scheduler; real customer reviews; swap
  stock photos for Grant's real job photos.

## Business details

- **Business name:** Elite Foam Insulation LLC · **Owner:** Grant (brother)
- **Live site:** https://elitesprayinsulation.com (also elite-foam-insulation.vercel.app)
- **Phone (click-to-call):** (904) 570-8897 — hidden in page source until "Call" is pressed
- **Lead alerts go to:** sulcata123@gmail.com (move to an `@elitesprayinsulation.com` inbox once Workspace is set up)
- **Service area:** Northeast Florida to Southeast Georgia
- **Services:** Full-service spray foam (open & closed cell; attics, crawlspaces, new construction, commercial)
- **Logo:** Real emblem in use (`frontend/logo.png`, cleaned from source) + favicon. Swap for a vector if the designer's file turns up.
- **Photos:** Stock spray-foam photos in use (`frontend/foam-*.jpg`) — replace with Grant's real job photos when available.
- **Brand:** Clean / industrial. Tagline "Seal it once. Save for decades." Brand color: royal blue.
- **Domain:** elitesprayinsulation.com — registrar + DNS at Cloudflare.

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
