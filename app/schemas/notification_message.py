from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId
from pydantic import BaseModel

class NotificationOut(BaseModel):
    id: PydanticObjectId
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    receiver_id: PydanticObjectId
    content: str

class MessageOut(BaseModel):
    id: PydanticObjectId
    sender_id: PydanticObjectId
    receiver_id: PydanticObjectId
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
