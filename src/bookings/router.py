from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.service import BookingService
from src.bookings.schemas import BookingSchema
from src.database import get_async_session
from src.exceptions import BookingException
from src.users.dependencies import get_current_user
from src.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("")
async def get_bookings(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)]
) -> list[BookingSchema]:
    return await BookingService.get_all_rows_by_filter(session, user_id=user.id)


@router.get("/{booking_id}")
def get_booking(booking_id):
    pass


@router.post("")
async def add_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    room_id: int,
    date_from: date,
    date_to: date,
    user: Annotated[User, Depends(get_current_user)]
):
    booking = await BookingService.add(session, user.id, room_id, date_from, date_to)
    if not booking:
        raise BookingException


@router.delete("/{booking_id}", dependencies=[Depends(get_current_user)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    booking_id: int
):
    await BookingService.delete_by_id(session, model_id=booking_id)
