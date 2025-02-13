from fastapi import APIRouter
from models.prescriptions import PrescriptionModel
from config.database import prescriptions as prescription_collection, patients as patient_collection
from bson import ObjectId
from schema.prescriptions import list_schema

prescription_router = APIRouter()

@prescription_router.get("/")
async def get_prescriptions():
    prescriptions = prescription_collection.find()
    return list_schema(prescriptions)

@prescription_router.post("/")
async def create_prescriptions(prescription: PrescriptionModel):
    json = prescription.model_dump()
    response = prescription_collection.insert_one(json)
    patientID = json["patientID"]
    patient = patient_collection.find_one({'_id': ObjectId(patientID)})

    if patient:
        old_prescriptions = patient.get('prescriptions', [])
        
        old_prescriptions.append(str(response.inserted_id))
        result = patient_collection.update_one(
            {'_id': ObjectId(patientID)},
            {"$set": {'prescriptions': old_prescriptions}}
        )
        
    return {"id": str(response.inserted_id)}
