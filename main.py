from fastapi import FastAPI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pydantic import BaseModel
from bson import ObjectId
from routes.routes import router
import os
from dotenv import load_dotenv

app = FastAPI()

app.include_router(router)