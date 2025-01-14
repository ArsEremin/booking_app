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

    class Config:
        model_config = ConfigDict(extra="forbid")
        orm_mode = True
