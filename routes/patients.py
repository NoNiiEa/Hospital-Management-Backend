from fastapi import APIRouter, HTTPException, status, Depends
from models.patients import PatientModel, GetPatientRequest, MedicalHistoryModel
from config.database import (
    patients as patients_collection, 
    doctors as doctor_collection, 
    appointments as appointment_collection, 
    prescriptions as prescription_collection
)
from schema.patients_schemas import list_patient_schema, individual_patient_schema
from bson import ObjectId
from starlette import status

patient_router = APIRouter()

@patient_router.get("/", status_code=status.HTTP_200_OK)
async def get_patients():
    patients = patients_collection.find()
    return list_patient_schema(patients)

@patient_router.get("/get/{patient_id}")
async def get_patient_individal(patient_id: str):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient id.")

    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")
    
    return individual_patient_schema(patient)

@patient_router.get("/limit/{page}/{limit}", status_code=status.HTTP_200_OK)
async def get_patientsLimit(page: int, limit: int):
    skip = (page - 1) * limit
    
    patients_cursor = patients_collection.find().skip(skip).limit(limit)
    patients = patients_cursor.to_list(length=limit)
    
    return list_patient_schema(patients)

@patient_router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_patients(patient: PatientModel):
    response = patients_collection.insert_one(patient.model_dump())
    return {"id": str(response.inserted_id)}

@patient_router.put("/medicalhistory/{patient_id}/")
async def add_medical_history(patient_id: str, medical_history: MedicalHistoryModel):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient ID.")

    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

    medical_history_dict = medical_history.model_dump()

    result = patients_collection.update_one(
        {"_id": ObjectId(patient_id)},
        {"$push": {"medical_history": {"$each": [medical_history_dict], "$position": 0}}}
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update medical history.")

    return {"message": "Successfully updated medical history."}

    

@patient_router.delete("/delete/{patient_id}", status_code=status.HTTP_200_OK)
async def delete_patient(patient_id: str):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid patient id."
        )
    
    obj_id = ObjectId(patient_id)
    
    result = patients_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Patient not found"
        )
    
    doctor_collection.update_many(
        {"patients.patient_id": patient_id}, 
        {"$pull": {"patients": {"patient_id": patient_id}}}
    )

    appointment_collection.delete_many({"patient_id": patient_id})
    prescription_collection.delete_many({"patient_id": patient_id})
    
    return {"message": "Patient deleted successfully"}
