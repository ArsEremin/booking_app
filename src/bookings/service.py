from datetime import date

from sqlalchemy import select, or_, func, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.models import Booking
from src.hotels.models import Room
from src.services.base import BaseService


class BookingService(BaseService):
    model = Booking

    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        """with booked_rooms as (
            select * from booking
            where room_id = ... and
            (date_from < ... or date_to > ...)
            )
            select room.quantity - count(booked_rooms.room_id) from room
            left join booked_rooms on booked_rooms.room_id = room.id
            where room.id = ...
            group by room.id"""

        booked_rooms = (
            select(Booking)
            .where(
                Booking.room_id == room_id,
                or_(
                    Booking.date_from < date_to,
                    Booking.date_to > date_from
                )
            )
        ).cte("booked_rooms")

        get_remaining_rooms = (
            select((Room.quantity - func.count(booked_rooms.c.room_id)).label("remaining_rooms"))
            .join(booked_rooms, isouter=True)
            .where(Room.id == room_id)
            .group_by(Room.id)
        )

        print(get_remaining_rooms.compile(compile_kwargs={"literal_binds": True}))

        remaining_rooms = await session.execute(get_remaining_rooms)
        remaining_rooms = remaining_rooms.scalar()
        if remaining_rooms > 0:
            get_price = select(Room.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price = price.scalar()

            add_booking = (
                insert(Booking)
                .values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                )
            ).returning(Booking)

            new_booking = await session.execute(add_booking)
            new_booking = new_booking.scalar()
            await session.commit()
            return new_booking
        else:
            return None
