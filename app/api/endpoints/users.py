from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from beanie import PydanticObjectId
import os
import uuid
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.user import UserOut
from app.schemas.user_update import UserUpdate, PasswordUpdate
from app.core.security import get_password_hash, verify_password
from app.api.deps import get_current_user
from app.core.cloudinary import upload_image

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserOut)
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user)
):
    update_data = user_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(current_user, field, update_data[field])
    
    await current_user.save()
    return current_user

@router.post("/me/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    password_in: PasswordUpdate,
    current_user: User = Depends(get_current_user)
):
    if not verify_password(password_in.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")
    
    current_user.password_hash = get_password_hash(password_in.new_password)
    await current_user.save()
    return {"message": "Mot de passe mis à jour avec succès"}

@router.post("/me/favorites/{vehicle_id}")
async def add_favorite(
    vehicle_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    # Vérifier si le véhicule existe
    vehicle = await Vehicle.get(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    if vehicle_id not in current_user.favorites:
        current_user.favorites.append(vehicle_id)
        await current_user.save()
    
    return {"message": "Véhicule ajouté aux favoris"}

@router.delete("/me/favorites/{vehicle_id}")
async def remove_favorite(
    vehicle_id: PydanticObjectId,
    current_user: User = Depends(get_current_user)
):
    if vehicle_id in current_user.favorites:
        current_user.favorites.remove(vehicle_id)
        await current_user.save()
    
    return {"message": "Véhicule retiré des favoris"}

from beanie.operators import In
from app.schemas.vehicle import VehicleOut

@router.get("/me/favorites", response_model=List[VehicleOut])
async def list_favorites(current_user: User = Depends(get_current_user)):
    # Peupler les détails des véhicules favoris
    vehicles = await Vehicle.find(In(Vehicle.id, current_user.favorites), fetch_links=True).to_list()
    return vehicles

@router.post("/me/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    url = await upload_image(file.file, folder="avatars")
    if not url:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload de l'avatar")
    
    # Si on veut stocker l'URL dans le profil
    # current_user.avatar_url = url
    # await current_user.save()
    
    return {"avatar_url": url, "message": "Avatar uploadé avec succès"}
