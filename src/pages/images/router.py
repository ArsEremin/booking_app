import shutil

from fastapi import UploadFile, status
from src.pages.router import router


@router.post("/images", status_code=status.HTTP_201_CREATED)
async def add_hotel_image(image_id: int, file: UploadFile):
    with open(f"src/static/images/{image_id}.webp", "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
