from datetime import date

from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import MappedColumn, mapped_column, relationship
from src.database import Base


class Booking(Base):
    __tablename__ = "booking"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    room_id = mapped_column(ForeignKey("room.id", onupdate="CASCADE", ondelete="RESTRICT"))
    user_id = mapped_column(ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"))
    date_from: MappedColumn[date] = mapped_column(nullable=False)
    date_to: MappedColumn[date] = mapped_column(nullable=False)
    price: MappedColumn[int] = mapped_column(nullable=False)
    total_cost: MappedColumn[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: MappedColumn[int] = mapped_column(Computed("date_to - date_from"))

    user: MappedColumn["User"] = relationship(back_populates="bookings")
    room: MappedColumn["Room"] = relationship(back_populates="bookings")
