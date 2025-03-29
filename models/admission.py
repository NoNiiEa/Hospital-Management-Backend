from pydantic import BaseModel, field_validator
from typing import List, Optional
from bson import ObjectId
from config.database import patients as patient_collection
from models.billing import BillingModel

class TreatmentModel(BaseModel):
    procedure: str
    scheduled_date: str
    status: str

class MedicationModel(BaseModel):
    name: str
    dosage: str
    frequency: str
    duration: str

class InsuranceModel(BaseModel):
    provider: str
    policy_number: str
    coverage: str
    amount_covered: int
    amount_due: int

class AdmissionModel(BaseModel):
    patient_id: str
    admission_date: str
    expected_discharge_date: str
    actual_discharge_date: Optional[str] = None
    doctor_id: str
    department: str
    admission_reason: str
    ward: str
    bed_number: str
    status: str
    treatment_plan: List[TreatmentModel]
    medications: List[MedicationModel]
    billing: Optional[BillingModel] = None

    @field_validator("patient_id", mode="before")
    @classmethod
    def validate_patient_id(cls, patient_id):
        """Validate if the given patient_id exists in the database."""
        if not ObjectId.is_valid(patient_id):
            raise ValueError("Invalid ObjectId format")

        # Check if the patient exists in the database
        patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            raise ValueError(f"Patient with ID {patient_id} not found in the database")

        return str(patient_id)
