from fastapi import APIRouter
from models.patients import PatientModel
from config.database import patients as patients_collection
from schema.patients_schemas import list_patient_schema

patient_router = APIRouter()

@patient_router.get("/")
async def get_patients():
    patients = patients_collection.find()
    return list_patient_schema(patients)

@patient_router.post("/")
async def create_patients(patient: PatientModel):
    response = patients_collection.insert_one(patient.model_dump())
    return {"id": str(response.inserted_id)}