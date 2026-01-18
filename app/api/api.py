from fastapi import APIRouter
from app.api.endpoints import auth, vehicles, bookings, users, agencies

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(agencies.router, prefix="/agencies", tags=["agencies"])
