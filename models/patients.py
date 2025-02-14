from pydantic import BaseModel
from typing import List

class ContactModel(BaseModel):
    phone: str
    email: str
    address: str

class MedicalHistoryModel(BaseModel):
    disease: str
    diagnosed_date: str
    treatment: str

class PatientModel(BaseModel):
    name: str
    age: int
    gender: str
    contact: ContactModel
    medical_history: List[MedicalHistoryModel]
    appointments: List[str]
    prescriptions: List[str]