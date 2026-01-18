from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.agency import Agency
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.reservation import Reservation
from app.schemas.agency import AgencyOut, AgencyUpdate, AgencyStats
from app.api.deps import get_current_user

router = APIRouter()

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
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency:
        raise HTTPException(status_code=404, detail="Profil d'agence non trouvé")

    # Statistiques
    total_vehicles = await Vehicle.find(Vehicle.agency_id == agency.id).count()
    reservations = await Reservation.find(Reservation.vehicle_id.in_([v.id async for v in Vehicle.find(Vehicle.agency_id == agency.id)])).to_list()
    
    total_reservations = len(reservations)
    total_revenue = sum(r.total_price for r in reservations if r.status == "completed" or r.status == "confirmed")
    
    # Véhicules les plus vus
    most_viewed = await Vehicle.find(Vehicle.agency_id == agency.id).sort("-views").limit(5).to_list()
    
    return {
        "total_vehicles": total_vehicles,
        "total_reservations": total_reservations,
        "total_revenue": total_revenue,
        "most_viewed_vehicles": [v.model_dump() for v in most_viewed]
    }
