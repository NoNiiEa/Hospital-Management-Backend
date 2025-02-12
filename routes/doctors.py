from fastapi import APIRouter
from models.doctors import DoctorModel
from config.database import doctors as doctors_collection
from schema.doctor_schemas import list_doctor_schema

doctor_router = APIRouter()

@doctor_router.get("/")
async def get_doctors():
    doctors = doctors_collection.find()
    return list_doctor_schema(doctors)

@doctor_router.post("/")
async def create_doctors(doctor: DoctorModel):
    response = doctors_collection.insert_one(doctor.model_dump())
    return {"id": str(response.inserted_id)}