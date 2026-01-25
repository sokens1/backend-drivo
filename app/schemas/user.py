from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., alias="name")
    phone: str

    class Config:
        populate_by_name = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)
    role: Optional[str] = "client"
    agency_name: Optional[str] = None

class UserOut(UserBase):
    id: PydanticObjectId
    role: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
