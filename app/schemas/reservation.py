from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from beanie import PydanticObjectId

class ReservationBase(BaseModel):
    vehicle_id: PydanticObjectId
    start_date: datetime
    end_date: datetime
    payment_method: str # "orange_money", "airtel_money", "card"
    type: str # "location", "vente"

class ReservationCreate(ReservationBase):
    pass

class ReservationOut(ReservationBase):
    id: PydanticObjectId
    user_id: PydanticObjectId
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
