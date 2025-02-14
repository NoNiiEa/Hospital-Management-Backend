from fastapi import APIRouter, HTTPException
from models.doctors import DoctorModel
from config.database import doctors as doctors_collection, appointments as appointment_collection, prescriptions as prescription_collection
from schema.doctor_schemas import list_doctor_schema
from bson import ObjectId

doctor_router = APIRouter()

@doctor_router.get("/")
async def get_doctors():
    doctors = doctors_collection.find()
    return list_doctor_schema(doctors)

@doctor_router.post("/create")
async def create_doctors(doctor: DoctorModel):
    response = doctors_collection.insert_one(doctor.model_dump())
    return {"id": str(response.inserted_id)}

@doctor_router.delete("/delete/{doctor_id}")
async def delete_doctor(doctor_id: str):
    result = doctors_collection.delete_one({"_id": ObjectId(doctor_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Doctor with that ID: {doctor_id} not found")
    
    appointment_collection.update_many(
        {"doctor_id": str(ObjectId(doctor_id))},
        {"$set" : {"doctor_id": "N/A"}}
    )

    prescription_collection.update_many(
        {"doctor_id": str(ObjectId(doctor_id))},
        {"$set": {"doctor_id": "N/A"}}
    )
    
    return {"result" : f"Doctor with ID: {doctor_id} has successfully deleted"}