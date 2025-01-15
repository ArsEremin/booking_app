from src.bookings.models import Booking
from src.services.base import BaseService


class BookingService(BaseService):
    model = Booking
