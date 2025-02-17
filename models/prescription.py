from pydantic import BaseModel, field_validator
from typing import List
from config.database import patients as patient_collection, doctors as doctor_collection
from bson import ObjectId

class MedicationModel(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str

class PrescriptionModel(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    medications: List[MedicationModel]
