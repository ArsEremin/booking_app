from datetime import date

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.models import Booking
from src.hotels.models import Hotel, Room
from src.hotels.schemas import HotelSchema, HotelWithNumSchema
from src.services.base import BaseService


class HotelService(BaseService):
    model = Hotel

    @classmethod
    async def get_free_hotels(
        cls,
        session: AsyncSession,
        location: str,
        date_from: date,
        date_to: date
    ):
        booked_rooms = (
            select(Booking)
            .where(
                or_(
                    Booking.date_from < date_to,
                    Booking.date_to > date_from
                )
            )
        ).subquery("booked_rooms")

        get_booked_rooms_num = (
            select(Room.hotel_id, func.count(booked_rooms.c.room_id).label("booked_rooms_number"))
            .join(booked_rooms, isouter=True)
            .group_by(Room.hotel_id)
        ).cte("get_booked_rooms_num")

        get_free_hotels = (
            select(Hotel, (Hotel.rooms_quantity - get_booked_rooms_num.c.booked_rooms_number).label("free_room_num"))
            .join(get_booked_rooms_num)
            .where(
                Hotel.location.contains(location),
                Hotel.rooms_quantity - get_booked_rooms_num.c.booked_rooms_number > 0
            )
        )

        free_hotels = await session.execute(get_free_hotels)

        free_hotels_dto = []
        for hotel, free_rooms_num in free_hotels:
            free_hotels_dto.append(
                HotelWithNumSchema(free_rooms_number=free_rooms_num, **HotelSchema.model_validate(hotel).dict())
            )
        return free_hotels_dto
