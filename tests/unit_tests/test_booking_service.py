from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.service import BookingService


class TestBookingService:
    async def test_add_booking(self, session: AsyncSession):
        new_booking = await BookingService.add(
            session,
            user_id=2,
            room_id=2,
            date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
            date_to=datetime.strptime("2023-07-24", "%Y-%m-%d")
        )

        assert new_booking and new_booking.user_id == 2 and new_booking.room_id == 2

    async def test_get_booking_by_id(self, session: AsyncSession):
        booking = await BookingService.get_by_id(session, model_id=2)
        assert booking and booking.user_id == 2 and booking.room_id == 7

    async def test_delete_booking_by_id(self, session: AsyncSession):
        await BookingService.delete_by_id(session, model_id=3)
        bookings = await BookingService.get_by_id(session, model_id=3)
        assert not bookings
