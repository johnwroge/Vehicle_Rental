import unittest
from datetime import datetime, timedelta
from models import Booking

class TestBookingClass(unittest.TestCase):
    def setUp(self):
        """Setup default dates for testing"""
        self.current_date = datetime(2024, 1, 1, 10, 0, 0)
        
    def create_booking(self, pickup_date: datetime, return_date: datetime) -> Booking:
        """Helper to create booking with proper datetime format"""
        return Booking(
            user_id=1,
            vehicle_id=101,
            pickup_date=pickup_date.strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=return_date.strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=100.0
        )

    def test_booking_duration_exceeds_limit(self):
        """Test booking duration > 7 days"""
        pickup_date = self.current_date
        return_date = pickup_date + timedelta(days=8)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertIn("Booking duration cannot exceed 7 days", errors)

    def test_booking_duration_within_limit(self):
        """Test booking duration <= 7 days"""
        pickup_date = self.current_date
        return_date = pickup_date + timedelta(days=7)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertNotIn("Booking duration cannot exceed 7 days", errors)

    def test_advance_booking_exceeds_limit(self):
        """Test booking > 7 days in advance"""
        now = datetime.now()
        pickup_date = now + timedelta(days=8, hours=12)
        return_date = pickup_date + timedelta(days=3)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertIn("Cannot book more than 7 days in advance", errors)

    def test_advance_booking_within_limit(self):
        """Test booking <= 7 days in advance"""
        pickup_date = self.current_date + timedelta(days=7)
        return_date = pickup_date + timedelta(days=3)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertNotIn("Cannot book more than 7 days in advance", errors)

    def test_return_date_before_pickup(self):
        """Test return date before pickup date"""
        pickup_date = self.current_date
        return_date = pickup_date - timedelta(days=1)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertIn("Return date must be after pickup date", errors)

    def test_valid_booking(self):
        """Test completely valid booking"""
        now = datetime.now()
        pickup_date = now + timedelta(days=1)
        return_date = pickup_date + timedelta(days=5)
        booking = self.create_booking(pickup_date, return_date)
        errors = booking.validate_dates()
        self.assertEqual([], errors)

if __name__ == "__main__":
    unittest.main(verbosity=2)