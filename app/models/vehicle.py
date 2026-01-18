from datetime import datetime
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import Field

class Vehicle(Document):
    agency_id: PydanticObjectId
    title: str
    brand: str
    model: str
    year: int
    price: float
    price_per_day: Optional[float] = None
    type: str  # "vente", "location", "both"
    category: str # "suv", "sedan", etc.
    images: List[str] = []
    km: int
    fuel: str
    transmission: str
    location: str
    features: List[str] = []
    description: str
    views: int = 0
    available: bool = True
    adapted_roads: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "vehicles"
