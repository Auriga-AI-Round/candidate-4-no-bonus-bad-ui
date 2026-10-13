"""Hospital management — FastAPI + SQLAlchemy on PostgreSQL.

Full core: patients, doctors, appointments with the 30-minute overlap rejection at
the data layer, search, and billing. No analytics dashboard / landing page.
"""

from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        and_, create_engine, or_)
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5432/hospital")
Session = sessionmaker(bind=engine)
Base = declarative_base()
SLOT = timedelta(minutes=30)


class Patient(Base):
    __tablename__ = "patient"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, index=True)
    email = Column(String)


class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    specialization = Column(String, index=True)
    fee = Column(Float, default=0)


class Appointment(Base):
    __tablename__ = "appointment"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patient.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctor.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="booked")


Base.metadata.create_all(engine)
app = FastAPI()


class BookIn(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: str


@app.post("/api/appointments", status_code=201)
def book(data: BookIn):
    try:
        start = datetime.fromisoformat(data.start_time)
    except ValueError:
        raise HTTPException(400, "invalid start_time")
    end = start + SLOT
    s = Session()
    # Overlap twist: reject any overlap for the same doctor (half-open interval).
    overlap = (
        s.query(Appointment)
        .filter(
            Appointment.doctor_id == data.doctor_id,
            Appointment.status == "booked",
            and_(Appointment.start_time < end, Appointment.end_time > start),
        )
        .first()
    )
    if overlap:
        s.close()
        raise HTTPException(409, "doctor already booked in an overlapping slot")
    appt = Appointment(patient_id=data.patient_id, doctor_id=data.doctor_id,
                       start_time=start, end_time=end)
    s.add(appt); s.commit(); aid = appt.id; s.close()
    return {"id": aid}


@app.get("/api/patients")
def list_patients(q: str = ""):
    s = Session()
    query = s.query(Patient)
    if q:
        query = query.filter(or_(Patient.name.ilike(f"%{q}%"), Patient.phone.ilike(f"%{q}%")))
    rows = [{"id": p.id, "name": p.name, "phone": p.phone} for p in query.all()]
    s.close()
    return rows


@app.get("/api/doctors")
def list_doctors(specialization: str = ""):
    s = Session()
    query = s.query(Doctor)
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
    rows = [{"id": d.id, "name": d.name, "specialization": d.specialization} for d in query.all()]
    s.close()
    return rows


@app.get("/api/doctors/{doctor_id}/billing")
def billing(doctor_id: int):
    s = Session()
    doc = s.get(Doctor, doctor_id)
    if not doc:
        s.close()
        raise HTTPException(404, "doctor not found")
    completed = (s.query(Appointment)
                 .filter(Appointment.doctor_id == doctor_id,
                         Appointment.status == "completed").count())
    total = completed * (doc.fee or 0)
    s.close()
    return {"doctor_id": doctor_id, "completed": completed, "total_billed": total}
