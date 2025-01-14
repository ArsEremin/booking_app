from fastapi import APIRouter

from bookings.service import BookingService
from bookings.shemas import BookingSchema

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get("")
async def get_bookings() -> list[BookingSchema]:
    return await BookingService.get_all_rows()


@router.get("/{booking_id}")
def get_booking(booking_id):
    pass
