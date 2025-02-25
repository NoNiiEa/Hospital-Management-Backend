from pydantic import BaseModel, field_validator
from typing import List, Literal, Optional
from bson import ObjectId
from config.database import patients as patient_collection 
from config.database import appointments as appointment_collection 

class BillingModel(BaseModel):
    patient_id: str
    appointment_id: str
    total_amount: int
    status :Literal["Paid","Not Paid"]
    payment_method : Literal["Credit Card","insurance", "cash"]

class UpdateStatusRequest(BaseModel):
    status: Literal["Paid","Not Paid"]