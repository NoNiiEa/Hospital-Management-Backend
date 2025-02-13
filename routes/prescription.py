from fastapi import APIRouter
from models.prescription import PrescriptionModel
from config.database import prescriptions as prescription_collection, patients as patient_collection
from schema.prescription import list_schema
from bson import ObjectId

prescription_router = APIRouter()

@prescription_router.get("/")
async def get_prescriptions():
    prescriptions = prescription_collection.find()
    return list_schema(prescriptions)

@prescription_router.post("/")
async def create_prescriptions(prescription: PrescriptionModel):
    json = prescription.model_dump()
    response = prescription_collection.insert_one(json)

    patient_id = json["patient_id"]
    patient = patient_collection.find_one({"_id": ObjectId(patient_id)})

    if patient:
        old_prescriptions = patient.get("prescriptions", [])
        old_prescriptions.append(str(response.inserted_id))

        patient_collection.update_one(
            {"_id": ObjectId(patient_id)},
            {"$set": {"prescriptions": old_prescriptions}}
        )

    return {"id": str(response.inserted_id)}
