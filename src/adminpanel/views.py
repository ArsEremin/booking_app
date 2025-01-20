from sqladmin import ModelView

from src.bookings.models import Booking
from src.hotels.models import Room, Hotel
from src.users.models import User


class UserView(ModelView, model=User):
    column_list = [User.id, User.email, User.bookings]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class BookingView(ModelView, model=Booking):
    column_list = [column.name for column in Booking.__table__.columns] + [Booking.user, Booking.room]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"


class RoomView(ModelView, model=Room):
    column_list = [column.name for column in Room.__table__.columns] + [Room.bookings]
    name = "Комната"
    name_plural = "Комнаты"
    icon = "fa-solid fa-bed"


class HotelView(ModelView, model=Hotel):
    column_list = [column.name for column in Hotel.__table__.columns] + [Hotel.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"
