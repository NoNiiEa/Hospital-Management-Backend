from pydantic import BaseModel, field_validator
from typing import Literal
from bson import ObjectId
from config.database import patients as patient_collection, doctors as doctor_collection

class AppointmentModel(BaseModel):
    patient_id: str
    doctor_id: str
    date: str
    time: str
    status: Literal["Pending", "Confirmed", "Cancelled"]
    remarks: str
    
class UpdateStatusRequest(BaseModel):
    status: Literal["Pending", "Confirmed", "Cancelled"]
