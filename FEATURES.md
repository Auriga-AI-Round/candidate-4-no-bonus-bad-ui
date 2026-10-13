# Features

Implemented and verifiable in `main.py`.

- Patient management: list + search — `main.py:list_patients`
- Doctor management: list + specialization filter — `main.py:list_doctors`
- Appointment booking with **30-minute overlap rejection** (409) —
  `main.py:book` (half-open interval filter)
- Search: patients by name/phone, doctors by specialization — `main.py`
- Billing: completed appointments × fee — `main.py:billing`
- PostgreSQL via SQLAlchemy — `main.py` engine + `db/dump.sql`

## Not done (out of scope for this submission)
- Analytics dashboard / landing page — **not built**
- Patient/doctor create endpoints exist only partially (focus was booking correctness)

| Feature | Status |
|---|---|
| Patient list + search | ✅ |
| Doctor list + search | ✅ |
| Booking + overlap twist | ✅ |
| Billing | ✅ |
| Analytics dashboard | ❌ not done |
