from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import SessionCreate_Schema, SessionResponse_Schema

from app.services import (
    add_movie_session,
    get_all_movie_sessions
)


router = APIRouter(prefix="/sessions", tags=["Сеанси"])

@router.post("/")
async def movie_session_post(
    data: SessionCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> SessionResponse_Schema | None:
    
    movie_session = await add_movie_session(data, session)
    if movie_session is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Невірно введені дані"
        )
    return movie_session


@router.get("/")
async def movie_session_get_all(session: AsyncSession = Depends(get_db)) -> list[SessionResponse_Schema]:
    return await get_all_movie_sessions(session)