from fastapi import APIRouter, HTTPException
from models.doctors import DoctorModel, PatientModel
from config.database import doctors as doctors_collection, appointments as appointment_collection, prescriptions as prescription_collection, patients as patient_collection
from schema.doctor_schemas import list_doctor_schema
from bson import ObjectId
from starlette import status

doctor_router = APIRouter()

@doctor_router.get("/")
async def get_doctors():
    doctors = doctors_collection.find()
    return list_doctor_schema(doctors)

@doctor_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_doctors(doctor: DoctorModel):
    response = doctors_collection.insert_one(doctor.model_dump())
    return {"id": str(response.inserted_id)}

@doctor_router.put("/{doctor_id}/add_patient/{patient_id}")
async def add_patient(patient_id: str, doctor_id: str):
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    list_patient = doctor.get("patients", [])
    
    for patient0 in list_patient:
        if patient0["patient_id"] == patient_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Patient already in the Doctor's patient list"
            )

    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    medical_history = patient.get("medical_history", [{}])
    diagnosis = medical_history[0].get("disease", "N/A")
    last_visit = medical_history[0].get("diagnosed_date", "N/A")

    new_patient = PatientModel(patient_id=patient_id, diagnosis=diagnosis, last_visit=last_visit)
    list_patient.insert(0, new_patient.model_dump())
    
    result = doctors_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$set": {"patients": list_patient}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to add patient")

    return {"result": "success"}


@doctor_router.delete("/delete/{doctor_id}")
async def delete_doctor(doctor_id: str):
    result = doctors_collection.delete_one({"_id": ObjectId(doctor_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Doctor with ID: {doctor_id} not found")
    
    appointment_collection.update_many(
        {"doctor_id": str(ObjectId(doctor_id))},
        {"$set": {"doctor_id": "N/A"}}
    )

    prescription_collection.update_many(
        {"doctor_id": str(ObjectId(doctor_id))},
        {"$set": {"doctor_id": "N/A"}}
    )
    
    return {"result": f"Doctor with ID: {doctor_id} has been successfully deleted"}
