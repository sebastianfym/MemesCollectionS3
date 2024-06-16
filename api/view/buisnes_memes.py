from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from api.routers.buisnes_router import router
from api.utilities import decode_img
from config.config import settings
from db.config import get_db
from schemas.memes.models import MemeCRUD, Meme
from db.models.memes import Memes

from services.services import upload_file_to_s3


@router.post("", status_code=HTTP_201_CREATED, response_model=Meme)
async def memes_create(meme: MemeCRUD, db: AsyncSession = Depends(get_db)) -> Meme:
    """Создание мема"""
    image_file = decode_img(meme)
    image_data = upload_file_to_s3(image_file, settings.S3_BUCKET_NAME)
    if "error" in image_data:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=image_data["error"])

    db_meme = Memes(title=meme.title, image_url=image_data["url"])
    db.add(db_meme)
    await db.commit()
    await db.refresh(db_meme)
    return db_meme


@router.put("/{id}", status_code=HTTP_200_OK, response_model=Meme)
async def memes_update(id: int, meme: MemeCRUD, db: AsyncSession = Depends(get_db)) -> Meme | None:
    """Обновление мема"""
    db_meme = await db.get(Memes, id)
    if not db_meme:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Meme not found")

    for key, value in meme.dict().items():
        if value is not None:
            setattr(db_meme, key, value)
        if key == "image_url":
            image_file = decode_img(meme)
            image_data = upload_file_to_s3(image_file, settings.S3_BUCKET_NAME)
            setattr(db_meme, key, image_data['url'])
    updated_meme = Meme(
        id=db_meme.id,
        title=db_meme.title,
        image_url=db_meme.image_url,
    )
    await db.commit()
    await db.refresh(db_meme)
    return updated_meme


@router.delete("/{id}", status_code=HTTP_200_OK, response_model=None)
async def memes_delete(id: int, db: AsyncSession = Depends(get_db)) -> {}:
    """Удаление мема"""
    db_meme = await db.get(Memes, id)
    if not db_meme:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Meme not found")

    await db.delete(db_meme)
    await db.commit()
    return {"detail": "Meme deleted"}
