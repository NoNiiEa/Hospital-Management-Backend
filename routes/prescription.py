from fastapi import APIRouter, HTTPException
from models.prescription import PrescriptionModel
from config.database import prescriptions as prescription_collection, patients as patient_collection, doctors as doctor_collection
from schema.prescription import list_schema
from bson import ObjectId
from starlette import status

prescription_router = APIRouter()

@prescription_router.get("/")
async def get_prescriptions():
    prescriptions = prescription_collection.find()
    return list_schema(prescriptions)

@prescription_router.post("/create")
async def create_prescriptions(prescription: PrescriptionModel):
    json = prescription.model_dump()
    response = prescription_collection.insert_one(json)

    patient_id = json["patient_id"]
    doctor_id = json["doctor_id"]

    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Patient ID")
    if not ObjectId.is_valid(doctor_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Doctor ID")

    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})
    doctor = doctor_collection.find_one({"_id": ObjectId(doctor_id)})
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id: {doctor_id} not found.")

    if patient:
        old_prescriptions = patient.get("prescriptions", [])
        old_prescriptions.append(str(response.inserted_id))

        patient_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": {"prescriptions": old_prescriptions}}
        )
    else :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id:{patient_id} not found.")

    return {"id": str(response.inserted_id)}
