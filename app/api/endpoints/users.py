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

@router.get("/me/favorites", response_model=List[PydanticObjectId])
async def list_favorites(current_user: User = Depends(get_current_user)):
    return current_user.favorites

@router.post("/me/avatar", status_code=status.HTTP_200_OK)
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    upload_dir = "uploads/avatars"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    avatar_url = f"/uploads/avatars/{filename}"
    # On pourrait ajouter un champ avatar_url au modèle User
    return {"avatar_url": avatar_url, "message": "Avatar uploadé avec succès"}
