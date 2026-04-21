from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.model_appointment import Appointment
from app.schemas.appointment import AppointmentCreate, AppointmentRead

router = APIRouter()


# CREATE APPOINTMENT
@router.post("/", response_model=AppointmentRead)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    appointment = Appointment(**data.dict())

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment


# GET ALL APPOINTMENTS
@router.get("/", response_model=list[AppointmentRead])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(Appointment).all()


# GET APPOINTMENTS BY PATIENT (NEW)
@router.get("/patient/{patient_id}", response_model=list[AppointmentRead])
def get_appointments_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()


# UPDATE STATUS
@router.patch("/{appointment_id}")
def update_status(appointment_id: int, status: str, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = status
    db.commit()

    return {"message": "Status updated"}