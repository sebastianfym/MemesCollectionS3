import base64
from io import BytesIO
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


def decode_img(meme):
    try:
        image_bytes = base64.b64decode(meme.image_url)
        image_file = BytesIO(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"{e}")
    return image_file
