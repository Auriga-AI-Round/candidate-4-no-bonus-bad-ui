# Hospital Management (FastAPI + PostgreSQL)

Backend-focused submission. Full appointment core with the 30-minute overlap rule,
search and billing on PostgreSQL. The UI is a single plain operational table; there is
**no analytics dashboard / landing page** (left out due to time).

## Setup
```bash
pip install fastapi uvicorn sqlalchemy "psycopg[binary]"
createdb hospital
uvicorn main:app --port 8000
```

## Docs
- `FEATURES.md`, `API.md` — feature + endpoint list
- `REASONING.md` — the overlap design
- `AI_LOG.md` — AI usage
- `db/dump.sql` — PostgreSQL schema
- `tests/` — overlap tests

## Submission
App URL: http://localhost:8000
API base: http://localhost:8000/api
Username: reviewer@example.com
Password: review-pass-123
Endpoints:
  - GET /api/patients
  - GET /api/doctors
  - POST /api/appointments
  - GET /api/doctors/{id}/billing
Notes: Postgres-backed; booking enforces a 30-min overlap rule. No landing page.
