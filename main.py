from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.routes import router
from dotenv import load_dotenv
import os

env_file = ".env"
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    print("⚠️ Warning: .env file not found! Ensure it exists before running the app.")

frontend_url = os.getenv("frontend")

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)