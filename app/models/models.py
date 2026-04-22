from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Movie_Model(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float | None] = mapped_column()

class Hall_Model(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    hall_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    rows: Mapped[int] = mapped_column(nullable=False)
    seats_per_row: Mapped[int] = mapped_column(nullable=False)

class Movie_Session_Model(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="CASCADE"), nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id", ondelete="CASCADE"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    movie: Mapped["Movie_Model"] = relationship(back_populates="sessions")
    hall: Mapped["Hall_Model"] = relationship(back_populates="sessions")