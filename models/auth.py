from pydantic import BaseModel
from typing import Optional

class Users(BaseModel):
    username: str
    hashed_password: str
    role: str = "user"
    role_id: Optional[str] = None

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    