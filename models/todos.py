from pydantic import BaseModel

class TodoModel(BaseModel):
    title: str
    description: str
    completed: bool