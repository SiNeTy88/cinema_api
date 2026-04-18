from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

from app.models import User_Model
from app.schemas import UserCreate_Schema, UserResponse_Schema

from app.core.security import get_password_hash, verify_password, security, configx

async def get_user_by_email(email, session: AsyncSession) -> User_Model:
    query = select(User_Model).where(User_Model.email == email)
    result = await session.execute(query)
    return result.scalars().first()
    
async def create_user(user_data: UserCreate_Schema, session: AsyncSession) -> User_Model:
    hashed_pwd = get_password_hash(user_data.password)

    new_user = User_Model(
        email = user_data.email,
        hashed_password = hashed_pwd
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user

# async def register_user(
#     user_data: UserCreate_Schema,
#     session: AsyncSession = Depends(get_db)
# ):
#     # query = select(User_Model).where(User_Model.email == user_data.email)
#     # result = await session.execute(query)
#     # existing_user = result.scalars().first()
#     res = await get_user_by_email(user_data, session)
#     if res:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Користувач з таким email вже зареєстрований"
#         )
    
#     hashed_pwd = get_password_hash(user_data.password)

#     new_user = User_Model(
#         email = user_data.email,
#         hashed_password = hashed_pwd
#     )
#     session.add(new_user)
#     await session.commit()
#     await session.refresh(new_user)

#     return new_user
    
# async def login_user(
#     user_data: UserCreate_Schema,
#     response: Response,
#     session: AsyncSession = Depends(get_db),
#     ):
#     res = await get_user_by_email(user_data, session)

#     if not res or not verify_password(user_data.password, res.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, 
#             detail="Невірний email або пароль"
#         )
#     token = security.create_access_token(uid=str(res.id))

#     response.set_cookie(configx.JWT_ACCESS_COOKIE_NAME, token)

#     return {"access_token": token, "token_type": "bearer"}