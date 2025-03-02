from fastapi import APIRouter, HTTPException
from config.database import staffs as staff_collection
from schema.staff import list_schema, individual_schema
from models.staffs import StaffModel
from bson import ObjectId
from starlette import status

router = APIRouter()

@router.get("/")
async def get_staff():
    staffs = staff_collection.find()
    return list_schema(staffs)

@router.post("/create")
async def create_staff(staff: StaffModel):
    response = staff_collection.insert_one(staff.model_dump())
    return {"id": str(response.inserted_id)}

@router.get("/get/{staff_id}")
async def get_individual_staff(staff_id: str):
    if not ObjectId.is_valid(staff_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid staff id.")
    staff = staff_collection.find_one({"_id": ObjectId(staff_id)})
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff id not found.")
    return individual_schema(staff)

@router.get("/limit/{page}/{limit}")
async def get_doctor_limit(page: int, limit: int):
    skip = (page - 1) * limit
    
    satff_cursor = staff_collection.find().skip(skip).limit(limit)
    staffs = list(satff_cursor)
    
    return list_schema(staffs)

@router.delete("/delete/{staff_id}")
async def delete_staff(staff_id: str):
    if not ObjectId.is_valid(staff_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid staff id.")
    result = staff_collection.delete_one({"_id": ObjectId(staff_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Staff with id: {staff_id} not found.")
    return {"result" : f"Staff with id: {staff_id} has successfully deleted."}







