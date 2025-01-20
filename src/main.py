from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from redis import asyncio as aioredis

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin

from src.adminpanel.auth import authentication_backend
from src.adminpanel.views import UserView, BookingView, RoomView, HotelView
from src.bookings.router import router as router_bookings
from src.config import settings
from src.database import engine
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
    allow_headers=["Content-Type", "Set-Cookie", "Authorization","Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin"]
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserView)
admin.add_view(BookingView)
admin.add_view(RoomView)
admin.add_view(HotelView)
