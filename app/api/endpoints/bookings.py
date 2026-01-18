from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from app.models.reservation import Reservation
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationOut
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/create", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_in: ReservationCreate,
    current_user: User = Depends(get_current_user)
):
    # Vérifier si le véhicule existe
    vehicle = await Vehicle.get(reservation_in.vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Véhicule non trouvé")
    
    # Vérifier la disponibilité
    if not vehicle.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce véhicule n'est plus disponible."
        )

    # Calcul du prix total
    total_price = 0.0
    if reservation_in.type == "location":
        if not vehicle.price_per_day:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce véhicule n'est pas disponible à la location."
            )
        delta = reservation_in.end_date - reservation_in.start_date
        days = max(delta.days, 1) # Au moins 1 jour
        total_price = days * vehicle.price_per_day
    else:
        total_price = vehicle.price

    new_reservation = Reservation(
        **reservation_in.model_dump(),
        user_id=current_user.id,
        total_price=total_price,
        status="pending"
    )
    
    await new_reservation.insert()
    return new_reservation

@router.get("/", response_model=List[ReservationOut])
async def list_user_reservations(current_user: User = Depends(get_current_user)):
    reservations = await Reservation.find(Reservation.user_id == current_user.id).to_list()
    return reservations
