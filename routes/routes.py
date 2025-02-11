from fastapi import APIRouter, HTTPException

from models.todos import TodoModel
from models.patients import PatientModel
from config.database import patients as patients_collection
from schema.patients_schemas import list_patient_schema
from bson import ObjectId

router = APIRouter()

# @router.get("/todos")
# async def get_todos():
#     todos = collection_name.find()
#     return list_schema(todos)

# @router.post("/todos")
# async def create_todos(todo: TodoModel):
#     response = collection_name.insert_one(dict(todo))
#     return {"id": str(response.inserted_id)}

# @router.get("/todos/{id}")
# async def get_todo_by_id(id: str):
#     todo = collection_name.find_one({"_id": ObjectId(id)})
#     if todo:
#         return individual_schema(todo)
#     raise HTTPException(status_code=404, detail="Todo not found")

@router.get("/patients")
async def get_patients():
    patients = patients_collection.find()
    return list_patient_schema(patients)

@router.post("/patients")
async def create_patients(patient: PatientModel):
    response = patients_collection.insert_one(patient.model_dump())
    return {"id": str(response.inserted_id)}

