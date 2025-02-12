from pymongo import MongoClient
from dotenv import load_dotenv
import os

env_file = ".env"
if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    print("⚠️ Warning: .env file not found! Ensure it exists before running the app.")

uri = os.getenv("uri")

if not uri:
    raise ValueError("❌ Error: MongoDB URI not found. Set 'uri' in the .env file.")

# Connect to MongoDB
client = MongoClient(uri)
db = client.hosbitalDB
patients = db["patients"]
doctors = db["doctors"]
appointments = db["appountments"]