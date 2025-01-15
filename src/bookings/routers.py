from typing import Annotated

from fastapi import APIRouter, Depends

from src.bookings.service import BookingService
from src.bookings.schemas import BookingSchema
from src.users.dependencies import get_current_user
from src.users.models import User

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings(user: Annotated[User, Depends(get_current_user)]) -> list[BookingSchema]:
    return await BookingService.get_all_rows_by_filter(user_id=user.id)


@router.get("/{booking_id}")
def get_booking(booking_id):
    pass
