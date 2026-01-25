from datetime import datetime
from typing import List, Optional
from beanie import Document, PydanticObjectId
from pydantic import Field

class User(Document):
    email: str
    password_hash: str
    full_name: str
    phone: str
    role: str = "client"  # "client", "agence", "admin"
    is_verified: bool = True
    favorites: List[PydanticObjectId] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
