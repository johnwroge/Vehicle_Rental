from enum import Enum

class BookingStatus(Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class VehicleStatus(Enum):
    AVAILABLE = 'available'
    RENTED = 'rented'
    MAINTENANCE = 'maintenance'