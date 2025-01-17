from datetime import date

from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.models import Booking
from src.hotels.models import Room
from src.hotels.rooms.schemas import RoomSchema, ExtendedRoomSchema
from src.services.base import BaseService


class RoomService(BaseService):
    model = Room

    @classmethod
    async def get_free_rooms(
        cls,
        session: AsyncSession,
        hotel_id: int,
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

        get_free_rooms_num = (
            select(Room.id, (Room.quantity - func.count(booked_rooms.c.room_id)).label("free_rooms_number"))
            .join(booked_rooms, isouter=True)
            .group_by(Room.id)
        ).cte("get_free_rooms_num")

        get_only_free_rooms = (
            select(Room, get_free_rooms_num.c.free_rooms_number, Room.price * (date_to - date_from).days)
            .join(get_free_rooms_num, Room.id == get_free_rooms_num.c.id)
            .where(Room.hotel_id == hotel_id, get_free_rooms_num.c.free_rooms_number > 0)
        )

        free_rooms = await session.execute(get_only_free_rooms)

        free_rooms_dto = []
        for room, free_rooms_num, total_cost in free_rooms:
            free_rooms_dto.append(
                ExtendedRoomSchema(
                    free_rooms_number=free_rooms_num,
                    total_cost=total_cost,
                    **RoomSchema.model_validate(room).dict()
                )
            )
        return free_rooms_dto
