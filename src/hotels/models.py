from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from src.database import Base


class Hotel(Base):
    __tablename__ = "hotel"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    name: MappedColumn[str] = mapped_column(nullable=False)
    location: MappedColumn[str] = mapped_column(nullable=False)
    services = mapped_column(JSON)
    rooms_quantity: MappedColumn[int] = mapped_column(nullable=False)
    image_id: MappedColumn[int]

    rooms: MappedColumn["Room"] = relationship(
        back_populates="hotel"
    )


class Room(Base):
    __tablename__ = "room"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    hotel_id: MappedColumn[int] = mapped_column(
        ForeignKey("hotel.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )
    name: MappedColumn[str] = mapped_column(nullable=False)
    description: MappedColumn[str] = mapped_column(nullable=True)
    price: MappedColumn[int] = mapped_column(nullable=False)
    services = mapped_column(JSON)
    quantity: MappedColumn[int] = mapped_column(nullable=False)
    image_id: MappedColumn[int]

    hotel: MappedColumn["Hotel"] = relationship(
        back_populates="rooms"
    )
