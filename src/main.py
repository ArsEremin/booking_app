from typing import Annotated

from fastapi import FastAPI, Query
from datetime import date

from pydantic import BaseModel

from bookings.shemas import BookingSchema
from src.bookings.routers import router as router_bookings
from src.users.routers import router as router_users

app = FastAPI()

app.include_router(router_users)
app.include_router(router_bookings)


class HotelSchema(BaseModel):
    name: str
    address: str
    stars: str


@app.get("/hotels", response_model=list[HotelSchema])
def get_hotels(
    location: Annotated[str, Query(max_length=50)],
    date_from: date,
    date_to: date,
    has_spa: bool | None = None,
    start: Annotated[int | None, Query(ge=1, le=5)] = None
):
    hotels = [{"name": "a", "address": "sada", "starts": "1"}]
    return hotels


@app.post("/bookings")
def add_booking(booking: BookingSchema):
    pass
