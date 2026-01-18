from typing import Optional
from beanie import Document, PydanticObjectId

class Agency(Document):
    user_id: PydanticObjectId
    name: str
    logo_url: Optional[str] = None
    address: str
    phone: str
    verified: bool = False
    rating: float = 0.0
    
    class Settings:
        name = "agencies"
