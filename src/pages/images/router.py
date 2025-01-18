import shutil

from fastapi import UploadFile, status

from src.pages.router import router
from src.tasks.tasks import resize_image


@router.post("/images", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(image_id: int, file: UploadFile):
    image_path = f"src/static/images/{image_id}.webp"
    with open(image_path, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    resize_image.delay(image_path)
