-- SprayFoam — Supabase schema (Phase 1)
-- A single table to capture contact-form submissions (leads).
-- Run this in the Supabase SQL Editor (Dashboard > SQL Editor > New query).
--
-- Security model:
--   * The backend uses the SERVICE_ROLE key, which BYPASSES RLS — it owns all writes.
--   * The browser never touches this table directly; it POSTs to the FastAPI /contact
--     endpoint. So we enable RLS and add NO public policies (default-deny for anon).

create table if not exists leads (
    id           uuid primary key default gen_random_uuid(),
    created_at   timestamptz not null default now(),
    name         text not null,
    email        text,
    phone        text,
    -- What kind of work / message the customer described.
    message      text,
    -- Optional: which service they were interested in, the page/source, etc.
    service      text,
    source       text,
    -- Owner workflow: track follow-up without a separate CRM at first.
    status       text not null default 'new'
                     check (status in ('new','contacted','quoted','won','lost'))
);

create index if not exists idx_leads_created on leads (created_at desc);
create index if not exists idx_leads_status  on leads (status);

-- Enable RLS with no anon policies → the anon/public key cannot read or write.
-- Only the service_role (backend) can touch this table.
alter table leads enable row level security;
