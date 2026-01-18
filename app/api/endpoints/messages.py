from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId
from app.models.message import Message
from app.models.user import User
from app.schemas.notification_message import MessageCreate, MessageOut
from app.api.deps import get_current_user
from motor.core import AgnosticCollection

router = APIRouter()

@router.get("/", response_model=List[MessageOut])
async def list_messages(current_user: User = Depends(get_current_user)):
    """Récupère tous les messages envoyés ou reçus par l'utilisateur"""
    messages = await Message.find(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).sort("-created_at").to_list()
    return messages

@router.post("/", response_model=MessageOut)
async def send_message(message_in: MessageCreate, current_user: User = Depends(get_current_user)):
    # Vérifier que le destinataire existe
    receiver = await User.get(message_in.receiver_id)
    if not receiver:
        raise HTTPException(status_code=404, detail="Destinataire non trouvé")
    
    new_message = Message(
        sender_id=current_user.id,
        receiver_id=message_in.receiver_id,
        content=message_in.content
    )
    await new_message.insert()
    return new_message
