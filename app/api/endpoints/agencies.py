from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
import os
import uuid
from beanie.operators import In
from app.models.agency import Agency
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.reservation import Reservation
from app.schemas.agency import AgencyOut, AgencyUpdate
from app.schemas.dashboard import AgencyStats
from app.api.deps import get_current_user
from app.core.cloudinary import upload_image

router = APIRouter()

@router.get("/", response_model=List[AgencyOut])
async def list_agencies(skip: int = 0, limit: int = 20):
    """Liste publique de toutes les agences"""
    agencies = await Agency.find().skip(skip).limit(limit).to_list()
    return agencies

@router.get("/me", response_model=AgencyOut)
async def get_my_agency(current_user: User = Depends(get_current_user)):
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency:
        raise HTTPException(status_code=404, detail="Profil d'agence non trouvé")
    return agency

@router.patch("/me", response_model=AgencyOut)
async def update_my_agency(
    agency_in: AgencyUpdate,
    current_user: User = Depends(get_current_user)
):
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency:
        # Créer si n'existe pas
        agency = Agency(user_id=current_user.id, **agency_in.model_dump())
        await agency.insert()
    else:
        update_data = agency_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(agency, field, update_data[field])
        await agency.save()
    return agency

@router.get("/dashboard", response_model=AgencyStats)
async def get_agency_dashboard(current_user: User = Depends(get_current_user)):
    try:
        agency = await Agency.find_one(Agency.user_id == current_user.id)
        if not agency:
            raise HTTPException(status_code=404, detail="Profil d'agence non trouvé")

        # Statistiques
        agency_vehicles = await Vehicle.find(Vehicle.agency.id == agency.id).to_list()
        total_vehicles = len(agency_vehicles)
        total_views = sum(int(v.views or 0) for v in agency_vehicles)
        
        vehicle_ids = [v.id for v in agency_vehicles]
        
        # Correction de l'opérateur IN pour Beanie
        reservations = await Reservation.find(In(Reservation.vehicle_id, vehicle_ids)).to_list()
        
        total_reservations = len(reservations)
        total_revenue = sum(float(r.total_price or 0.0) for r in reservations if r.status in ["completed", "confirmed"])
        
        # Véhicules les plus vus
        most_viewed = await Vehicle.find(Vehicle.agency.id == agency.id).sort("-views").limit(5).to_list()
        
        return AgencyStats(
            total_vehicles=int(total_vehicles),
            total_views=int(total_views),
            total_reservations=int(total_reservations),
            total_revenue=float(total_revenue),
            most_viewed_vehicles=most_viewed
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur technique Dashboard: {str(e)}"
        )

@router.post("/me/logo", status_code=status.HTTP_200_OK)
async def upload_agency_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency:
        raise HTTPException(status_code=404, detail="Profil d'agence non trouvé")
        
    url = await upload_image(file.file, folder="logos")
    if not url:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload du logo")
    
    agency.logo_url = url
    await agency.save()
    return {"logo_url": agency.logo_url, "message": "Logo uploadé avec succès"}
