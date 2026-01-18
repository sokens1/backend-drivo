from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification_message import NotificationOut
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[NotificationOut])
async def list_notifications(current_user: User = Depends(get_current_user)):
    notifications = await Notification.find(Notification.user_id == current_user.id).sort("-created_at").to_list()
    return notifications

@router.patch("/{id}/read")
async def mark_notification_as_read(id: PydanticObjectId, current_user: User = Depends(get_current_user)):
    notification = await Notification.get(id)
    if not notification or notification.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    
    notification.is_read = True
    await notification.save()
    return {"status": "ok"}
