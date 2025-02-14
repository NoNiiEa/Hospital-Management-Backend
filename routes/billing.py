from fastapi import APIRouter,HTTPException
from models.billing import BillingModel
from config.database import billing as billing_collection
from config.database import appointments as appointment_collection
from config.database import patients as patients_collection
from schema.billing_schemas import list_billing_schema
from bson import ObjectId
from starlette import status

billing_router = APIRouter()

@billing_router.get("/")
async def get_billing():
    billings = billing_collection.find()
    return list_billing_schema(billings)



@billing_router.post("/create")
async def create_billings(billing: BillingModel):
    json = billing.model_dump()
    response = billing_collection.insert_one(json)

    patient_id = json["patient_id"]
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Patient ID")
    patient = patients_collection.find_one({"_id": ObjectId(patient_id)})
    
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Patient with id:{patient_id} not found.")
    return {"id": str(response.inserted_id)}

@billing_router.delete("/delete/{billing_id}")
async def delete_billings(billing_id: str):
    result = billing_collection.delete_one({"_id": ObjectId(billing_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Billing with that ID: {billing_id} not found")
    
    return {"result": f"Billing with ID: {billing_id} has successfully deleted"}
