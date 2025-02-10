from fastapi import APIRouter, HTTPException

from models.todos import TodoModel
from config.database import collection_name
from schema.schemas import individual_schema, list_schema
from bson import ObjectId

router = APIRouter()

@router.get("/todos")
async def get_todos():
    todos = collection_name.find()
    return list_schema(todos)

@router.post("/todos")
async def create_todos(todo: TodoModel):
    response = collection_name.insert_one(dict(todo))
    return {"id": str(response.inserted_id)}

