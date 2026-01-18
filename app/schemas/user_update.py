from typing import Optional
from pydantic import BaseModel

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
