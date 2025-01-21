from datetime import date
from typing import Annotated

from fastapi import Depends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.hotels.rooms.schemas import ExtendedRoomSchema
from src.hotels.rooms.service import RoomService
from src.hotels.router import router


@router.get("/{hotel_id}/rooms", response_model=list[ExtendedRoomSchema])
@cache(expire=30)
async def get_hotel_rooms(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hotel_id: int,
    date_from: date,
    date_to: date
):
    hotel_rooms = await RoomService.get_free_rooms(session, hotel_id, date_from, date_to)
    return hotel_rooms
