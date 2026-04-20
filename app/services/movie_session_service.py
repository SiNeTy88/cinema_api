from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Movie_Session_Model, Movie_Model, Hall_Model
from app.schemas import SessionCreate_Schema, SessionResponse_Schema


async def add_movie_session(
    data: SessionCreate_Schema, 
    session: AsyncSession,
    ) -> Movie_Model:
    
    movie = await session.get(Movie_Model, data.movie_id)
    hall = await session.get(Hall_Model, data.hall_id)

    # if not movie:
    #     raise HTTPException(status_code=404, detail="Фільм з таким ID не знайдено")
    if not movie or not hall:
        return None
    
    # if not hall:
    #     raise HTTPException(status_code=404, detail="Зал з таким ID не знайдено")
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


async def get_all_movie_sessions(session: AsyncSession) -> list[Movie_Model]:
    query = select(Movie_Session_Model).options(
            selectinload(Movie_Session_Model.movie),
            selectinload(Movie_Session_Model.hall)
    )
    
    result = await session.execute(query)
    return result.scalars().all()