from pydantic import BaseModel
from typing import Optional
from beanie import PydanticObjectId

class PaymentInitiate(BaseModel):
    reservation_id: PydanticObjectId
    phone_number: str # Format: 07xxxxxx ou 06xxxxxx (Gabon)
    amount: float

class PaymentCallback(BaseModel):
    transaction_id: str
    status: str # "SUCCESS", "FAILED"
    message: Optional[str] = None
    reference: str
