from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import HallCreate_Schema, HallResponse_Schema

from app.services import add_hall

router = APIRouter(prefix="/halls", tags=["Кінозали"])

@router.post("/")
async def hall_post(
    data: HallCreate_Schema, 
    session: AsyncSession = Depends(get_db),
    ) -> HallResponse_Schema:
    return await add_hall(data, session)