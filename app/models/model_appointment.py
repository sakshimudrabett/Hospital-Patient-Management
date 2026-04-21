from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_name = Column(String(255))
    date_time = Column(String(255))
    status = Column(String(50), default="scheduled")