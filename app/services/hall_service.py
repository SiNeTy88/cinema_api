from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Hall_Model
from app.schemas import HallCreate_Schema, HallResponse_Schema

async def add_hall(
    data: HallCreate_Schema, 
    session: AsyncSession
    ) -> HallResponse_Schema:
    hall = Hall_Model(**data.model_dump())
    session.add(hall)
    await session.commit()
    await session.refresh(hall)
    return hall