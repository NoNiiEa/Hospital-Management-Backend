from fastapi import APIRouter
from models.appointment import AppointmentModel
from config.database import appointments as appointment_collection
from schema.appointment import list_schema

appointment_router = APIRouter()

@appointment_router.get("/")
async def get_appointments():
    appointments = appointment_collection.find()
    return list_schema(appointments)

@appointment_router.post("/")
async def create_appointments(appointment: AppointmentModel):
    response = appointment_collection.insert_one(appointment.model_dump())
    return {"id": str(response.inserted_id)}

