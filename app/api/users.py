from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

from app.models import User_Model
from app.schemas import UserCreate_Schema, UserResponse_Schema

from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Користувачі"])

@router.post("/register", response_model=UserResponse_Schema, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate_Schema,
    session: AsyncSession = Depends(get_db)
):
    query = select(User_Model).where(User_Model.email == user_data.email)
    result = await session.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач з таким email вже зареєстрований"
        )
    
    hashed_pwd = get_password_hash(user_data.password)

    new_user = User_Model(
        email = user_data.email,
        hashed_password = hashed_pwd
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
    
