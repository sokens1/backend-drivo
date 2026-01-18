from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.reservation import Reservation
from app.models.agency import Agency
from app.models.notification import Notification
from app.models.message import Message
from app.api.api import api_router
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Drivo API", version="1.0.0")

# Configuration CORS pour autoriser le frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "https://drivo-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Créer le dossier uploads si il n'existe pas
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Servir les fichiers statiques
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_db_client():
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client.get_default_database(),
        document_models=[
            User,
            Vehicle,
            Reservation,
            Agency,
            Notification,
            Message
        ]
    )

@app.get("/")
async def root():
    return {"message": "Welcome to Drivo API", "status": "online"}
