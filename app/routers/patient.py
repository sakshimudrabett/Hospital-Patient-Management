from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.model_patient import Patient
from app.models.model_appointment import Appointment
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter()


# CREATE PATIENT
@router.post("/", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        age=patient.age,
        gender=patient.gender,
    )

    try:
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to create patient.")

    return db_patient


# GET ALL PATIENTS
@router.get("/", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    try:
        return db.query(Patient).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to fetch patients.")


# GET SINGLE PATIENT
@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    return patient


# UPDATE PATIENT
@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: Session = Depends(get_db),
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(patient, field, value)

    try:
        db.commit()
        db.refresh(patient)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Unable to update patient.")

    return patient


# DELETE PATIENT + RELATED APPOINTMENTS
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    try:
        # 🔥 delete related appointments first
        db.query(Appointment).filter(Appointment.patient_id == patient_id).delete()

        db.delete(patient)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Delete failed.")

    return {"message": "Patient and related appointments deleted"}