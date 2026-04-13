from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class Movie_Schema(BaseModel):
    title: str = Field(..., max_length=100, description="Назва фільму")
    description: str = Field(..., max_length=1000, description="Опис фільму")
    duration_minutes: int = Field(..., gt=0, description="Тривалість у хвилинах")
    rating: float = Field(..., ge=0, le=10, description="Рейтинг") 

class MovieCreate_Schema(Movie_Schema):
    pass

class MovieResponse_Schema(Movie_Schema):
    id: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)

class Hall_Schema(BaseModel):
    hall_name: str = Field(..., max_length=100, description="Назва залу")
    rows: int = Field(..., gt=0, description="Кількість рядів")
    seats_per_row: int = Field(..., gt=0, description="Кількість сидінь у ряду")

class HallCreate_Schema(Hall_Schema):
    pass

class HallResponse_Schema(Hall_Schema):
    id: int = Field(..., gt=0)

    model_config = ConfigDict(from_attributes=True)

class Session_Schema(BaseModel):
    movie_id: int = Field(..., gt=0, description="Фільм")
    hall_id: int = Field(..., gt=0, description="Кінозала")
    start_time: datetime = Field(..., description="Час початку сеансу")

class SessionCreate_Schema(Session_Schema):
    pass

class SessionResponse_Schema(Session_Schema):
    id: int = Field(..., gt=0)

    movie: MovieResponse_Schema 
    hall: HallResponse_Schema
    
    model_config = ConfigDict(from_attributes=True)