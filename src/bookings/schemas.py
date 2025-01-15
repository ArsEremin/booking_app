from datetime import date

from pydantic import BaseModel, ConfigDict


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(
        extra="forbid",  # дополнительные аргументы запрещены
        from_attributes=True  # для конвертации orm-моделей
    )
