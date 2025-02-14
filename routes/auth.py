from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi import APIRouter, HTTPException, Depends
from dotenv import load_dotenv
from models.auth import Users, CreateUserRequest, Token
from config.database import users as user_collection
from typing import Annotated
from datetime import timedelta, datetime
import jwt
from jwt import PyJWKError as JWTerror
import os

env_file = ".env"
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    print("⚠️ Warning: .env file not found! Ensure it exists before running the app.")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    existing_user = user_collection.find_one({"username": create_user_request.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = bcrypt_context.hash(create_user_request.password)

    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=hashed_password
    )

    response = user_collection.insert_one(create_user_model.model_dump())

    return {"message": "User created successfully", "user_id": str(response.inserted_id)}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user["username"], str(user["_id"]), timedelta(minutes=20))

    return {
        "access_token": token,
        "token_type": 'bearer'
    }

def authenticate_user(username: str, password: str):
    user = user_collection.find_one({"username": username})
    if not user:
        return False
    if not bcrypt_context.verify(password, user["hashed_password"]):
        return False
    return user

def create_access_token(username: str, id: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:    
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {"username": username, "_id": user_id}
    except JWTerror:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
