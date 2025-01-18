from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.bookings.router import router as router_bookings
from src.users.router import router as router_users
from src.hotels.rooms.router import router as router_rooms
from src.pages.images.router import router as router_fronted

app = FastAPI()

# монтируем отдельное приложение StaticFiles с названием static по адресу /static, картинки запрашиваются из src/static
app.mount("/static", StaticFiles(directory="src/static"), "static")

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_rooms)
app.include_router(router_fronted)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Authorization",
                  "Access-Control-Allow-Headers", "Access-Control-Allow-Origin"]
)
