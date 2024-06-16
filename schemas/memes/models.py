from pydantic import BaseModel


class MemeBase(BaseModel):
    id: int | None = None
    title: str | None


class MemeCRUD(MemeBase):
    title: str | None
    image_url: str = None


class Meme(MemeBase):
    id: int
    title: str
    image_url: str

    class Config:
        from_attributes = True
