from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.model_patient import Patient
from app.database import get_db
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter()


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


@router.get("/", response_model=list[PatientRead])
def list_patients(db: Session = Depends(get_db)):
    try:
        return db.query(Patient).all()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Unable to fetch patients.")


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    return patient


@router.patch("/{patient_id}", response_model=PatientRead)
def update_patient(patient_id: int, payload: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    try:
        db.commit()
        db.refresh(patient)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Update failed.")

    return patient


@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found.")

    try:
        db.delete(patient)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Delete failed.")

    return {"message": "Patient deleted"}