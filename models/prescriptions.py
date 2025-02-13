from pydantic import BaseModel, field_validator
from typing import List
from bson import ObjectId
from config.database import patients as patient_collection, doctors as doctor_collection


class MedicationModel(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str

class PrescriptionModel(BaseModel):
    patientID: str
    doctorID: str
    date: str
    medications: List[MedicationModel]

    @field_validator("patientID", mode="before")
    @classmethod
    def validate_patient_id(cls, patient_id):
        """Validate patient_id format and check existence in the database."""
        if not ObjectId.is_valid(patient_id):
            raise ValueError("Invalid ObjectId format for patient_id")

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found in the database")

        return str(patient_id)
    
    @field_validator("doctorID", mode="before")
    @classmethod
    def validate_doctor_id(cls, doctor_id):
        """Validate doctor_id format and check existence in the database."""
        if not ObjectId.is_valid(doctor_id):
            raise ValueError("Invalid ObjectId format for doctor_id")

        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
        if not doctor:
            raise ValueError(f"Doctor with ID {doctor_id} not found in the database")

        return str(doctor_id)



    