from fastapi import APIRouter, UploadFile

from src.services.images import ImagesService

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
async def upload_image(file: UploadFile):
    return await ImagesService().upload_image(file)

