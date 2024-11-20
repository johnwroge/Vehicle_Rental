
from repositories import UserRepository, BookingRepository
from models import User, Booking
from typing import List, Optional
from datetime import datetime

class BookingService:
    def __init__(self, booking_repo: BookingRepository):
        self.booking_repo = booking_repo

    def create_booking(self, booking_data: dict) -> int:
        booking = Booking(**booking_data)
        
        errors = booking.validate_dates()
        if errors:
            raise ValueError(", ".join(errors))
            
        return self.booking_repo.create(booking)
    
    def update_booking(self, booking_id: int, booking_data: dict) -> bool:
        updated_booking = Booking(**booking_data)
        errors = updated_booking.validate_dates()
        if errors:
            raise ValueError(", ".join(errors))
        return self.booking_repo.update(booking_id, updated_booking)

    def delete_booking(self, booking_id: int) -> bool:
        return self.booking_repo.delete(booking_id)

    def get_daily_report(self, date: datetime, category_id: Optional[int] = None) -> List[dict]:
        return self.booking_repo.get_daily_report(date, category_id)