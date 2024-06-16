from typing import List

from fastapi import HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from api.routers.public_router import router
from db.config import get_db
from schemas.memes.models import Meme
from db.models.memes import Memes


@router.get("", status_code=HTTP_200_OK, response_model=List[Meme])
async def memes_list(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)) -> List[Meme] | List[None]:
    """Список всех мемов"""
    result = await db.execute(select(Memes).offset(skip).limit(limit))
    memes = result.scalars().all()
    return memes


@router.get("/{id}", status_code=HTTP_200_OK, response_model=Meme)
async def memes_detail(id: int, db: AsyncSession = Depends(get_db)) -> Meme | None:
    """Детальное представление мема"""
    meme = await db.get(Memes, id)
    if not meme:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Meme not found")
    return meme



