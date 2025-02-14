from fastapi import APIRouter, HTTPException
from models.admission import AdmissionModel
from config.database import billing as admission_collection
from config.database import patients as patients_collection
from schema.admission_schemas import list_admission_schema
from bson import ObjectId

admission_router = APIRouter()

# Get all admissions
@admission_router.get("/")
async def get_admission():
    admissions = admission_collection.find()
    return list_admission_schema(admissions)

# Create new admission
@admission_router.post("/create")
async def create_admissions(admission: AdmissionModel):
    # Check if the patient_id exists in the databas
    json = admission.model_dump()
    patient_id = json["patient_id"]
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid ObjectId format for patient_id")
    
    patient = patients_collection.find_one({"_id": ObjectId(admission.patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient with ID {admission.patient_id} not found in the database")

    # Insert the admission record into the database
    response = admission_collection.insert_one(admission.model_dump())
    return {"id": str(response.inserted_id)}

# Delete admission by ID
@admission_router.delete("/delete/{admission_id}")
async def delete_admissions(admission_id: str):
    result = admission_collection.delete_one({"_id": ObjectId(admission_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Admission with ID {admission_id} not found")
    
    return {"result": f"Admission with ID {admission_id} has been successfully deleted"}
