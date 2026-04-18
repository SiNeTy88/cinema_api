from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Movie_Session_Model, Movie_Model, Hall_Model
from app.schemas import SessionCreate_Schema, SessionResponse_Schema

router = APIRouter(prefix="/sessions", tags=["Сеанси"])

@router.post("/")
async def movie_session_post(
    data: SessionCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> SessionResponse_Schema:
    
    movie = await session.get(Movie_Model, data.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Фільм з таким ID не знайдено")
    
    hall = await session.get(Hall_Model, data.hall_id)
    if not hall:
        raise HTTPException(status_code=404, detail="Зал з таким ID не знайдено")
    
    
    
    movie_session = Movie_Session_Model(**data.model_dump())
    session.add(movie_session)
    await session.commit()
    query = (
        select(Movie_Session_Model)
        .where(Movie_Session_Model.id == movie_session.id)
        .options(
            selectinload(Movie_Session_Model.movie),
            selectinload(Movie_Session_Model.hall)
        )
    )
    result = await session.execute(query)
    return result.scalar_one()


@router.get("/")
async def movie_session_get_all(session: AsyncSession = Depends(get_db)) -> list[SessionResponse_Schema]:
    query = select(Movie_Session_Model).options(
            selectinload(Movie_Session_Model.movie),
            selectinload(Movie_Session_Model.hall)
    )
    
    result = await session.execute(query)
    return result.scalars().all()