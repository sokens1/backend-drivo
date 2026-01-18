from datetime import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field

class Message(Document):
    sender_id: PydanticObjectId
    receiver_id: PydanticObjectId
    content: str
    is_read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "messages"
