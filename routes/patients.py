from fastapi import APIRouter, HTTPException
from models.patients import PatientModel, GetPatientRequest
from config.database import patients as patients_collection, doctors as doctor_collection, appointments as appointment_collection, prescriptions as prescription_collection
from schema.patients_schemas import list_patient_schema
from bson import ObjectId

patient_router = APIRouter()

@patient_router.get("/")
async def get_patients():
    patients = patients_collection.find()
    return list_patient_schema(patients)

@patient_router.post("/limit")
async def get_patientsLimit(request: GetPatientRequest):
    limit = request.limit;
    page = request.page
    skip = (page - 1) * limit
    patients = patients_collection.find().limit(limit).skip(skip).to_list(length=limit)
    return list_patient_schema(patients)

@patient_router.post("/create/")
async def create_patients(patient: PatientModel):
    response = patients_collection.insert_one(patient.model_dump())
    return {"id": str(response.inserted_id)}

@patient_router.delete("/delete/{patient_id}")
async def delete_patient(patient_id: str):
    result = patients_collection.delete_one({"_id": ObjectId(patient_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    obj_id = ObjectId(patient_id)
    
    doctor_collection.update_many(
        {"patients.patient_id": str(obj_id)}, 
        {"$pull": {"patients": {"patient_id": str(obj_id)}}}
    )

    appointment_collection.delete_many(
        {"patient_id": str(obj_id)}
    )

    prescription_collection.delete_many(
        {"patient_id": str(obj_id)}
    )
    
    return {"message": "Patient deleted successfully"}


