from fastapi import APIRouter
from config.database import patients as patients_collection
from schema.patients_schemas import list_patient_schema
from .patients import patient_router
from .doctors import doctor_router
from .appointment import appointment_router

router = APIRouter()

router.include_router(patient_router, prefix="/patients", tags=["patients"])
router.include_router(doctor_router, prefix="/doctors", tags=["doctors"])
router.include_router(appointment_router, prefix="/appointments", tags=["appointments"])


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


