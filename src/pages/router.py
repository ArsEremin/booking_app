from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.hotels.router import get_hotels
from src.hotels.schemas import HotelWithNumSchema

router = APIRouter(
    prefix="/frontend",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="src/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels: Annotated[list[HotelWithNumSchema], Depends(get_hotels)]
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )
