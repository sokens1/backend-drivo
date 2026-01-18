from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import Field

class Reservation(Document):
    vehicle_id: PydanticObjectId
    user_id: PydanticObjectId
    start_date: datetime
    end_date: datetime
    total_price: float
    status: str = "pending" # "pending", "confirmed", "completed", "cancelled"
    payment_method: str # "orange_money", "airtel_money", "card"
    type: str # "location", "vente"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reservations"
