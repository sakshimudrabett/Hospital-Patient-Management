from pydantic import BaseModel, ConfigDict
from typing import Optional

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    gender: str


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    age: int
    gender: str


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None