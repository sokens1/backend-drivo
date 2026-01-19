from typing import List
from pydantic import BaseModel
from app.schemas.vehicle import VehicleOut

class AgencyStats(BaseModel):
    total_vehicles: int
    total_views: int
    total_reservations: int
    total_revenue: float
    most_viewed_vehicles: List[VehicleOut]
