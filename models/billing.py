from pydantic import BaseModel, field_validator
from typing import List, Literal, Optional
from bson import ObjectId
from config.database import patients as patient_collection 
from config.database import appointments as appointment_collection 


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
    
class AppointmentModel(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str
    status: Literal["Pending", "Confirmed", "Cancelled"]
    remarks: str

    @field_validator("patient_id", mode="before")
    @classmethod
    def validate_patient_id(cls, patient_id):
        """Validate patient_id format and check existence in the database."""
        if not ObjectId.is_valid(patient_id):
            raise ValueError("Invalid ObjectId format for patient_id")

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found in the database")

        return str(patient_id)

    @field_validator("doctor_id", mode="before")
    @classmethod
    def validate_doctor_id(cls, doctor_id):
        """Validate doctor_id format and check existence in the database."""
        if not ObjectId.is_valid(doctor_id):
            raise ValueError("Invalid ObjectId format for doctor_id")

        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
        if not doctor:
            raise ValueError(f"Doctor with ID {doctor_id} not found in the database")

        return str(doctor_id)
    
class AppointmentModel(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str
    status: Literal["Pending", "Confirmed", "Cancelled"]
    remarks: str

    @field_validator("patient_id", mode="before")
    @classmethod
    def validate_patient_id(cls, patient_id):
        """Validate patient_id format and check existence in the database."""
        if not ObjectId.is_valid(patient_id):
            raise ValueError("Invalid ObjectId format for patient_id")

        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found in the database")

        return str(patient_id)

    @field_validator("doctor_id", mode="before")
    @classmethod
    def validate_doctor_id(cls, doctor_id):
        """Validate doctor_id format and check existence in the database."""
        if not ObjectId.is_valid(doctor_id):
            raise ValueError("Invalid ObjectId format for doctor_id")

        doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
        if not doctor:
            raise ValueError(f"Doctor with ID {doctor_id} not found in the database")

        return str(doctor_id)


class BillingModel(BaseModel):
    patient_id: str
    appointment_id: str
    total_amount: int
    status :Literal["Paid","Not Paid"]
    payment_method : Literal["Credit Card","insurance", "cash"]


'''
{
  "_id": ObjectId("bill_id"),
  "patient_id": ObjectId("patient_id"),
  "appointment_id": ObjectId("appointment_id"),
  "total_amount": 200,
  "status": "Paid", //Not paid
  "payment_method": "Credit Card" //insurance, cash
}
'''