from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Hall_Model
from app.schemas import HallCreate_Schema, HallResponse_Schema

router = APIRouter(prefix="/halls", tags=["Кінозали"])

@router.post("/")
async def hall_post(
    data: HallCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> HallResponse_Schema:
    hall = Hall_Model(**data.model_dump())
    session.add(hall)
    await session.commit()
    await session.refresh(hall)
    return hall