from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import MovieCreate_Schema, MovieResponse_Schema
from app.models import Movie_Model

router = APIRouter(prefix="/movies", tags=["Фільми"])

@router.post("/")
async def movie_post(
    data: MovieCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> MovieResponse_Schema:
    movie = Movie_Model(**data.model_dump())
    session.add(movie)
    await session.commit()
    await session.refresh(movie)
    return movie

@router.get("/")
async def movie_get_all(session: AsyncSession = Depends(get_db)) -> list[MovieResponse_Schema]:
    result = await session.execute(select(Movie_Model))
    movies = result.scalars().all()
    return movies

@router.get("/{id}")
async def movie_get_id(id: int, session: AsyncSession = Depends(get_db)) -> MovieResponse_Schema:
    movie = await session.get(Movie_Model, id)
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фільм з таким ID не знайдено"
        )
    return movie

@router.delete("/{id}")
async def movie_delete(id: int, session: AsyncSession = Depends(get_db)):
    movie = await session.get(Movie_Model, id)
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фільм з таким ID не знайдено"
        )
    await session.delete(movie)
    await session.commit()
    return {"message": f"Фільм {movie.title} успішно видалено"}