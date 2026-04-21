from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_name: str
    date_time: str


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_name: str
    date_time: str
    status: str

    class Config:
        from_attributes = True