from fastapi import APIRouter,HTTPException
from models.admission import AdmissionModel
from config.database import billing as admission_collection
# from config.database import appointments as appointment_collection
from config.database import patients as patients_collection
from schema.admission_schemas import list_admission_schema
from bson import ObjectId

admission_router = APIRouter()

@admission_router.get("/")
async def get_admission():
    admissions = admission_collection.find()
    return list_admission_schema(admissions)

@admission_router.post("/create")
async def create_admissions(admission: AdmissionModel):
    # Extract patient_id from the admission model
    patient_id = admission.patient_id

    # Check if the patient_id format is valid
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format for patient_id")
    
    # Check if the patient exists in the patients collection
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {patient_id} not found in the database")
    
    # If patient exists, insert the admission record into the admissions collection
    json = admission.model_dump()
    response = admission_collection.insert_one(json)

    return {"id": str(response.inserted_id)}



@admission_router.delete("/delete/{admission_id}")
async def delete_admissions(admission_id: str):
    result = admission_collection.delete_one({"_id": ObjectId(admission_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"admission with that ID: {admission_id} not found")
    
    return {"result": f"admission with ID: {admission_id} has successfully deleted"}
