from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
import os
import uuid
from app.models.agency import Agency
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.reservation import Reservation
from app.schemas.agency import AgencyOut, AgencyUpdate, AgencyStats
from app.api.deps import get_current_user

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
        agency_vehicles = await Vehicle.find(Vehicle.agency_id == agency.id).to_list()
        total_vehicles = len(agency_vehicles)
        
        # Sécurisation contre les valeurs nulles (si migrées de versions précédentes)
        total_views = sum((v.views or 0) for v in agency_vehicles)
        
        vehicle_ids = [v.id for v in agency_vehicles]
        reservations = await Reservation.find(Reservation.vehicle_id.in_(vehicle_ids)).to_list()
        
        total_reservations = len(reservations)
        total_revenue = sum((r.total_price or 0) for r in reservations if r.status in ["completed", "confirmed"])
        
        # Véhicules les plus vus (sécurisé)
        most_viewed = sorted(agency_vehicles, key=lambda x: (x.views or 0), reverse=True)[:5]
        
        return {
            "total_vehicles": total_vehicles,
            "total_views": total_views,
            "total_reservations": total_reservations,
            "total_revenue": total_revenue,
            "most_viewed_vehicles": [v.model_dump() for v in most_viewed]
        }
    except Exception as e:
        import traceback
        print(f"Dashboard Error: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur Dashboard: {str(e)}"
        )

@router.post("/me/logo", status_code=status.HTTP_200_OK)
async def upload_agency_logo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    agency = await Agency.find_one(Agency.user_id == current_user.id)
    if not agency:
        raise HTTPException(status_code=404, detail="Profil d'agence non trouvé")
    
    upload_dir = "uploads/logos"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(upload_dir, filename)
    
    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    agency.logo_url = f"/uploads/logos/{filename}"
    await agency.save()
    return {"logo_url": agency.logo_url, "message": "Logo uploadé avec succès"}
