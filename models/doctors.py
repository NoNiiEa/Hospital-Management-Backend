from pydantic import BaseModel, field_validator
from typing import List, Literal, Optional
from bson import ObjectId
from config.database import patients as patient_collection

class ContactModel(BaseModel):
    phone: str
    email: str
    address: str

class ScheduleModel(BaseModel):
    day: Literal["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    timeslot: List[str]

class PatientModel(BaseModel):
    patient_id: str
    diagnosis: Optional[str] = None
    last_visit: Optional[str] = None

class DoctorModel(BaseModel):
    name: str
    specialization: str
    contact: ContactModel
    schedule: List[ScheduleModel] = []
    patients: List[PatientModel] = []
