from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from .enums import BookingStatus

@dataclass
class Booking:
    user_id: int
    vehicle_id: int
    pickup_date: str
    return_date: str
    total_cost: float
    booking_id: Optional[int] = None
    status: BookingStatus = BookingStatus.PENDING
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.pickup_date = datetime.strptime(self.pickup_date, "%Y-%m-%dT%H:%M:%S")
        self.return_date = datetime.strptime(self.return_date, "%Y-%m-%dT%H:%M:%S")
        self.created_at = self.created_at or datetime.now()

    def validate_dates(self) -> List[str]:
        errors = []
        current_date = datetime.now()
        
        rental_duration = (self.return_date - self.pickup_date).days
        advance_days = (self.pickup_date - current_date).days
        
        if rental_duration > 7:
            errors.append("Booking duration cannot exceed 7 days")
        if advance_days > 7:
            errors.append("Cannot book more than 7 days in advance")
        if self.pickup_date >= self.return_date:
            errors.append("Return date must be after pickup date")
        if self.pickup_date < current_date:
            errors.append("Pickup date cannot be in the past")
            
        return errors
