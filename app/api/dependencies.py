from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User_Model

from app.core.security import security

async def get_current_user(
        token_payload = Depends(security.access_token_required),
        session: AsyncSession = Depends(get_db)
) -> User_Model:
    user_id = int(token_payload.sub)

    user = await session.get(User_Model, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Користувача не знайдено"
        )
    return user

async def get_admin_user(
        current_user: User_Model = Depends(get_current_user)
) -> User_Model:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостатньо прав. Ця дія дозволена тільки адміністраторам."
        )
    return current_user
