from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.payment import PaymentInitiate, PaymentCallback
from app.utils.airtel_money import AirtelMoneyService
from app.models.reservation import Reservation
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/airtel/collect", status_code=status.HTTP_200_OK)
async def collect_payment(
    payment_in: PaymentInitiate,
    current_user: User = Depends(get_current_user)
):
    # Vérifier que la réservation existe et appartient à l'utilisateur
    reservation = await Reservation.get(payment_in.reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    
    if reservation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorisé")

    # Appeler le service Airtel (Simulation)
    result = await AirtelMoneyService.initiate_payment(
        phone=payment_in.phone_number,
        amount=payment_in.amount,
        reference=str(reservation.id)
    )
    
    return result

@router.post("/airtel/callback")
async def airtel_callback(callback: PaymentCallback):
    # Logique pour traiter le retour d'Airtel
    # En simulation, on pourrait appeler cet endpoint manuellement ou via un script
    
    reservation = await Reservation.get(callback.reference)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation associée non trouvée")

    if callback.status == "SUCCESS":
        reservation.status = "confirmed"
        reservation.payment_method = "airtel_money"
    else:
        reservation.status = "failed"
    
    await reservation.save()
    return {"status": "ACK"}
