from datetime import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field

class Notification(Document):
    user_id: PydanticObjectId
    title: str
    message: str
    type: str  # "info", "success", "warning", "error"
    is_read: bool = False
    link: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "notifications"
