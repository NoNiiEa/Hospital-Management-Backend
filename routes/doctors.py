from fastapi import APIRouter, HTTPException, status
from models.doctors import DoctorModel
from config.database import (
    doctors as doctors_collection, 
    appointments as appointment_collection, 
    prescriptions as prescription_collection, 
    patients as patient_collection
)
from schema.doctor_schemas import list_doctor_schema, individual_doctor_schema
from bson import ObjectId

doctor_router = APIRouter()

@doctor_router.get("/", status_code=status.HTTP_200_OK)
async def get_doctors():
    doctors = doctors_collection.find()
    return list_doctor_schema(doctors)

@doctor_router.get("/get/{doctor_id}")
async def get_individual_doctor(doctor_id: str):
    if not ObjectId.is_valid(doctor_id):
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid doctor id.")
    
    doctor =  doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor id not found.")

    return individual_doctor_schema(doctor)
    
    
@doctor_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_doctors(doctor: DoctorModel):
    response = doctors_collection.insert_one(doctor.model_dump())
    return {"id": str(response.inserted_id)}

@doctor_router.put("/{doctor_id}/add_patient/{patient_id}", status_code=status.HTTP_200_OK)
async def add_patient(patient_id: str, doctor_id: str):
    if not ObjectId.is_valid(patient_id) or not ObjectId.is_valid(doctor_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid doctor or patient ID."
        )
    
    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Doctor not found"
        )
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Patient not found."
        )

    existing_patient = doctors_collection.find_one(
        {"_id": ObjectId(doctor_id), "patients.patient_id": patient_id}
    )
    
    if existing_patient:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Patient already in the Doctor's patient list"
        )

    update_result = doctors_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$addToSet": {"patients": {"patient_id": patient_id}}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to add patient"
        )
    
    return {"result": "success", "message": "Patient added to the doctor's list"}

@doctor_router.delete("/{doctor_id}/remove_patient/{patient_id}", status_code=status.HTTP_200_OK)
async def remove_patient_from_doctor(doctor_id: str, patient_id: str):
    if not ObjectId.is_valid(doctor_id) or not ObjectId.is_valid(patient_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid doctor or patient ID."
        )
    
    doctor = doctors_collection.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Doctor not found"
        )
    
    result = doctors_collection.update_one(
        {"_id": ObjectId(doctor_id)},
        {"$pull": {"patients": {"patient_id": patient_id}}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Patient not found in the Doctor's patient list"
        )

    return {"result": "success", "message": "Patient removed from the doctor's list"}

@doctor_router.delete("/delete/{doctor_id}", status_code=status.HTTP_200_OK)
async def delete_doctor(doctor_id: str):
    if not ObjectId.is_valid(doctor_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid doctor ID."
        )
    
    result = doctors_collection.delete_one({"_id": ObjectId(doctor_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Doctor with ID: {doctor_id} not found"
        )
    
    appointment_collection.update_many(
        {"doctor_id": doctor_id},
        {"$set": {"doctor_id": "N/A"}}
    )

    prescription_collection.update_many(
        {"doctor_id": doctor_id},
        {"$set": {"doctor_id": "N/A"}}
    )
    
    return {"result": "success", "message": f"Doctor with ID: {doctor_id} has been successfully deleted"}
