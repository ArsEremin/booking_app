from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from src.database import get_async_session
from src.hotels.schemas import HotelSchema, HotelWithNumSchema
from src.hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"]
)


@router.get("", response_model=list[HotelWithNumSchema])
@cache(expire=30)
async def get_hotels(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    location: Annotated[str, Query(max_length=100)],
    date_from: date,
    date_to: date,
):
    hotels = await HotelService.get_free_hotels(session, location, date_from, date_to)
    return hotels


@router.get("/{hotel_id}", response_model=HotelSchema)
async def get_hotel(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int
):
    hotel = await HotelService.get_by_id(session, model_id=hotel_id)
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="hotel is not found")
    return hotel


@router.post("/upload_hotels")
async def upload_hotels(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    file: UploadFile
) -> dict:
    hotels_data = pd.read_csv(file.file)

    for _, hotel_data in hotels_data.iterrows():
        hotel = {
            "name": hotel_data["name"],
            "location": hotel_data["location"],
            "services": hotel_data["services"].split(','),
            "rooms_quantity": hotel_data["rooms_quantity"],
            "image_id": hotel_data["image_id"]
        }

        await HotelService.add_row(
            session,
            **hotel
        )

    return {"status": "hotels uploaded successfully"}
