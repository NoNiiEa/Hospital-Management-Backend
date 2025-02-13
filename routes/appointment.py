from fastapi import APIRouter
from models.appointment import AppointmentModel
from config.database import appointments as appointment_collection, patients as patient_collection
from schema.appointment import list_schema
from bson import ObjectId

appointment_router = APIRouter()

@appointment_router.get("/")
async def get_appointments():
    appointments = appointment_collection.find()
    return list_schema(appointments)

@appointment_router.post("/")
async def create_appointments(appointment: AppointmentModel):
    json = appointment.model_dump()
    response = appointment_collection.insert_one(json)

    patient_id = json["patient_id"]
    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})

    if patient:
        old_appointments = patient["appointments"]
        old_appointments.append(str(response.inserted_id))
        result = patient_collection.update_one(
            {'_id': ObjectId(patient_id)},
            {"$set": {'appointments': old_appointments}}
        )
    return {"id": str(response.inserted_id)}

