from typing import List, Optional
from pydantic import BaseModel
from beanie import PydanticObjectId

class AgencyBase(BaseModel):
    name: str
    address: str
    phone: str
    logo_url: Optional[str] = None

class AgencyCreate(AgencyBase):
    pass

class AgencyUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    logo_url: Optional[str] = None

class AgencyOut(AgencyBase):
    id: PydanticObjectId
    user_id: PydanticObjectId
    verified: bool
    rating: float

    class Config:
        from_attributes = True

class AgencyStats(BaseModel):
    total_vehicles: int
    total_reservations: int
    total_revenue: float
    most_viewed_vehicles: List[dict]
