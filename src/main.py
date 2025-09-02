import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin
import uvicorn

from src.adminpanel.auth import authentication_backend
from src.adminpanel.views import BookingView, HotelView, RoomView, UserView
from src.bookings.router import router as router_bookings
from src.config import settings
from src.database import engine
from src.hotels.rooms.router import router as router_rooms
from src.logger import logger
from src.pages.images.router import router as router_fronted
from src.users.router import router as router_users

sentry_sdk.init(
    dsn="https://c0103c8445f221ba2805fc3f4bd43b55@o4508682231873536.ingest.de.sentry.io/4508682248519760",
    traces_sample_rate=1.0,
    _experiments={
        "continuous_profiling_auto_start": True,
    },
)

app = FastAPI()

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
    allow_headers=["Content-Type", "Set-Cookie", "Authorization", "Access-Control-Allow-Headers",
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


app = VersionedFastAPI(app, version_format='{major}', prefix_format='/v{major}')


admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserView)
admin.add_view(BookingView)
admin.add_view(RoomView)
admin.add_view(HotelView)

# монтируем отдельное приложение StaticFiles с названием static по адресу /static, картинки запрашиваются из src/static
app.mount("/static", StaticFiles(directory="src/static"), "static")


@app.middleware("http")
async def add_process_time_log(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request process time", extra={"process_time": round(process_time, 3)})
    return response


if __name__ == "__main__":
    uvicorn.run(
        app="src.main:app",
        host="127.0.0.1",
        port=8080
    )
