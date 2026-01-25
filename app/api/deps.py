from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from app.core.config import settings
from app.models.user import User
from app.schemas.token import TokenPayload

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl=f"/api/v1/auth/login"
)

async def get_current_user(token: str = Depends(reuseable_oauth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        print(f"DEBUG AUTH: Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Credentials validation error: {str(e)}",
        )
    
    # Debug log
    print(f"DEBUG AUTH: Payload sub (user_id): {token_data.sub}")
    
    user = await User.get(token_data.sub)
    if not user:
        print(f"DEBUG AUTH: User {token_data.sub} not found in database")
        raise HTTPException(status_code=404, detail="User not found")
    
    print(f"DEBUG AUTH: Authenticated as {user.email} ({user.role})")
    return user
