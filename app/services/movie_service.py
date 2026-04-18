from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import MovieCreate_Schema, MovieResponse_Schema
from app.models import Movie_Model


async def add_movie(
    data: MovieCreate_Schema, 
    session: AsyncSession
    ) -> MovieResponse_Schema:
    movie = Movie_Model(**data.model_dump())
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie

async def get_all_movies(session: AsyncSession) -> list[MovieResponse_Schema]:
    result = await session.execute(select(Movie_Model))
    return result.scalars().all()

async def get_movie_by_id(id: int, session: AsyncSession) -> MovieResponse_Schema:
    return await session.get(Movie_Model, id)


async def delete_movie(id: int, session: AsyncSession):
    movie = await session.get(Movie_Model, id)
    if movie is None:
        return False    
    await session.delete(movie)
    await session.commit()
    return True