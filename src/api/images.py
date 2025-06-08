from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post('')
async def upload_image(
        file: UploadFile,
        # background_tasks: BackgroundTasks
):
    image_path = f'src/static/images/{file.filename}'
    with open(image_path, "wb") as new_file:
        content = await file.read()
        new_file.write(content)

    resize_image.delay(image_path)
    # background_tasks.add_task(resize_image, image_path) как аналог, но плохой из-за малой вычислительной мощности
    # из-за того что задача запускается в новом потоке, а не в новом процессе


    return {"success": True}
