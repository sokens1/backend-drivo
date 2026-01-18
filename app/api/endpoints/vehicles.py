from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query, File, UploadFile
import os
import uuid
from beanie import PydanticObjectId
from app.models.vehicle import Vehicle
from app.models.user import User
from app.models.agency import Agency
from app.schemas.vehicle import VehicleCreate, VehicleOut, VehicleUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=VehicleOut, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_in: VehicleCreate,
    current_user: User = Depends(get_current_user)
):
    # Pour l'instant, on suppose que l'utilisateur est lié à une agence si il crée un véhicule
    # On pourrait vérifier le rôle ici (ex: "agence" ou "admin")
    if current_user.role not in ["agence", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Seules les agences peuvent ajouter des véhicules."
        )
    
    # Trouver l'agence associée à l'utilisateur
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency and current_user.role != "admin":
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil d'agence non trouvé pour cet utilisateur."
        )

    new_vehicle = Vehicle(
        **vehicle_in.model_dump(),
        agency_id=agency.id if agency else current_user.id, # Si admin sans agence, id user par défaut (à affiner)
        images=[] # Upload d'images à gérer plus tard
    )
    
    await new_vehicle.insert()
    return new_vehicle

@router.get("/", response_model=List[VehicleOut])
async def list_vehicles(
    brand: Optional[str] = None,
    type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    skip: int = 0,
    limit: int = 10
):
    query = {}
    if brand:
        query["brand"] = brand
    if type:
        query["type"] = type
    
    # Filtres de prix complexes avec MongoDB
    if min_price or max_price:
        price_query = {}
        if min_price:
            price_query["$gte"] = min_price
        if max_price:
            price_query["$lte"] = max_price
        query["price"] = price_query

    vehicles = await Vehicle.find(query).skip(skip).limit(limit).to_list()
    return vehicles

@router.get("/{id}", response_model=VehicleOut)
async def get_vehicle(id: PydanticObjectId):
    vehicle = await Vehicle.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    # Incrémenter les vues
    vehicle.views += 1
    await vehicle.save()
    
    return vehicle

@router.post("/{id}/images", response_model=VehicleOut)
async def upload_vehicle_images(
    id: PydanticObjectId,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user)
):
    vehicle = await Vehicle.get(id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    # Vérification des permissions
    if current_user.role not in ["agence", "admin"]:
        raise HTTPException(status_code=403, detail="Non autorisé")

    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    image_urls = []
    for file in files:
        # Générer un nom de fichier unique
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(upload_dir, filename)
        
        with open(filepath, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        image_urls.append(f"/uploads/{filename}")

    vehicle.images.extend(image_urls)
    await vehicle.save()
    return vehicle
