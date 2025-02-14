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

    @field_validator("patient_id", mode="before")
    @classmethod
    def validate_patient_id(cls, patient_id):
        """Validate if the given patient_id is a valid MongoDB ObjectId and exists in the database."""
        if not ObjectId.is_valid(patient_id):
            raise ValueError("Invalid ObjectId format")

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found in the database")

        return str(patient_id) 

    @field_validator("diagnosis", "last_visit", mode="before")
    @classmethod
    def fetch_patient_info(cls, value, info):
        """Fetch diagnosis and last visit from the database based on patient_id."""
        patient_id = info.data.get("patient_id")

        if not patient_id:
            return value 

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            return "N/A"

        if info.field_name == "diagnosis":
            return patient.get("medical_history", [{}])[0].get("disease", "N/A")
        elif info.field_name == "last_visit":
            return patient.get("medical_history", [{}])[0].get("diagnosed_date", "N/A")

        return value

class DoctorModel(BaseModel):
    name: str
    specialization: str
    contact: ContactModel
    schedule: List[ScheduleModel] = []
    patients: List[PatientModel] = []
