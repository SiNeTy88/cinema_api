from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import MovieCreate_Schema, MovieResponse_Schema
from app.models import Movie_Model

from app.services import (
    add_movie,
    get_all_movies,
    get_movie_by_id,
    delete_movie,
)

router = APIRouter(prefix="/movies", tags=["Фільми"])

@router.post("/")
async def movie_post(
    data: MovieCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> MovieResponse_Schema:
    return await add_movie(data, session)

@router.get("/")
async def movie_get_all(session: AsyncSession = Depends(get_db)) -> list[MovieResponse_Schema]:
    return await get_all_movies(session)

@router.get("/{id}")
async def movie_get_id(id: int, session: AsyncSession = Depends(get_db)) -> MovieResponse_Schema | None:
    movie = await get_movie_by_id(id, session)
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фільм з таким ID не знайдено"
        )
    return movie

@router.delete("/{id}")
async def movie_delete(id: int, session: AsyncSession = Depends(get_db)):
    movie = await delete_movie(id, session)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Фільм з таким ID не знайдено"
        )
    return {"message": "Фільм успішно видалено"}