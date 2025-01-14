from bookings.models import Booking
from services.base import BaseService


class BookingService(BaseService):
    model = Booking
