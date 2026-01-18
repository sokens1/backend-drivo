from typing import List, Optional
from pydantic import BaseModel
from beanie import PydanticObjectId
from datetime import datetime

class VehicleBase(BaseModel):
    title: str
    brand: str
    model: str
    year: int
    price: float
    price_per_day: Optional[float] = None
    type: str  # "vente", "location", "both"
    category: str
    km: int
    fuel: str
    transmission: str
    location: str
    features: List[str] = []
    description: str
    adapted_roads: bool = False

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    title: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    price: Optional[float] = None
    price_per_day: Optional[float] = None
    available: Optional[bool] = None

class VehicleOut(VehicleBase):
    id: PydanticObjectId
    agency_id: PydanticObjectId
    images: List[str]
    views: int
    available: bool
    created_at: datetime

    class Config:
        from_attributes = True
