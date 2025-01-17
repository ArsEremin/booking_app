from pydantic import BaseModel, ConfigDict


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str | None
    price: int
    services: list
    quantity: int
    image_id: int

    model_config = ConfigDict(from_attributes=True)


class ExtendedRoomSchema(RoomSchema):
    free_rooms_number: int
    total_cost: int
