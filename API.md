# API

Base `/api`. Each endpoint maps to a handler in `main.py`.

| Method | Path | Handler | Notes |
|---|---|---|---|
| POST | `/api/appointments` | `book` | 409 on 30-min overlap |
| GET | `/api/patients` | `list_patients` | `?q=` searches name/phone |
| GET | `/api/doctors` | `list_doctors` | `?specialization=` filters |
| GET | `/api/doctors/{id}/billing` | `billing` | completed × fee |

### Overlap rejected
```
POST /api/appointments { "patient_id":1, "doctor_id":2, "start_time":"2030-01-01T10:15:00" }
→ 409 { "detail": "doctor already booked in an overlapping slot" }
```
