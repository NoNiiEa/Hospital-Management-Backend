from fastapi import APIRouter,HTTPException
from models.admission import AdmissionModel
from config.database import admission as admission_collection
# from config.database import appointments as appointment_cllection
from config.database import patients as patients_collection
from schema.admission_schemas import list_admission_schema
from bson import ObjectId
from starlette import status

admission_router = APIRouter()

@admission_router.get("/")
async def get_admission():
    admissions = admission_collection.find()
    return list_admission_schema(admissions)



@admission_router.post("/create")
async def create_admissions(admission: AdmissionModel):
    json = admission.model_dump()
    response = admission_collection.insert_one(json)

    patient_id = json["patient_id"]
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Patient ID")
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id:{patient_id} not found.")
    return {"id": str(response.inserted_id)}

@admission_router.delete("/delete/{admission_id}")
async def delete_admissions(admission_id: str):
    if not ObjectId.is_valid(admission_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid admission id.")
    result = admission_collection.delete_one({"_id": ObjectId(admission_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"admission with that ID: {admission_id} not found")
    
    return {"result": f"admission with ID: {admission_id} has successfully deleted"}
