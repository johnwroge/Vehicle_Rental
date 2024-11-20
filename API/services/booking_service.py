
from repositories import UserRepository, BookingRepository
from models import User, Booking
from typing import List, Optional
from datetime import datetime

class BookingService:
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo

    def create_booking(self, booking_data: dict) -> int:
        booking = Booking(**booking_data)
        
        # Validate booking
        errors = booking.validate_dates()
        if errors:
            raise ValueError(", ".join(errors))
            
        # Create booking
        return self.booking_repo.create(booking)

    def get_daily_report(self, date: datetime, category_id: Optional[int] = None) -> List[dict]:
        return self.booking_repo.get_daily_report(date, category_id)