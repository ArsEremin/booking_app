from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi_versioning import version
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.schemas import BookingSchema
from src.bookings.service import BookingService
from src.database import get_async_session
from src.exceptions import BookingException
from src.logger import logger
from src.tasks.tasks import send_confirmation_email
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
async def get_booking(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
    booking_id: int
) -> BookingSchema:
    return await BookingService.get_by_filter(session, id=booking_id, user_id=user.id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    room_id: int,
    date_from: date,
    date_to: date,
    user: Annotated[User, Depends(get_current_user)]
):
    try:
        booking = await BookingService.add(session, user.id, room_id, date_from, date_to)
        if not booking:
            raise BookingException
        booking_dict = BookingSchema.model_validate(booking).dict()
        send_confirmation_email.delay(booking_dict, user.email)
        return booking_dict
    except SQLAlchemyError:
        msg = "Invalid transaction"
        extra = {"user_id": user.id, "room_id": room_id, "date_from": date_from, "date_to": date_to}
        logger.error(msg, extra=extra, exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/{booking_id}", dependencies=[Depends(get_current_user)], status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    booking_id: int
):
    await BookingService.delete_by_id(session, model_id=booking_id)
