from pydantic import BaseModel, ConfigDict


class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class HotelWithNumSchema(HotelSchema):
    free_rooms_number: int
