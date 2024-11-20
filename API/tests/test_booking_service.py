import unittest
from datetime import datetime, timedelta
from services.booking_service import BookingService
from repositories.booking_repository import BookingRepository
from models import Booking
from unittest.mock import Mock, patch

class TestBookingService(unittest.TestCase):
    def setUp(self):
        """Initialize test environment before each test"""
        self.booking_repo = Mock(spec=BookingRepository)
        self.booking_service = BookingService(self.booking_repo)

    def test_create_booking(self):
        """Test booking service"""
        booking_data = {
            "user_id": 1,
            "vehicle_id": 1,
            "pickup_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "return_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "total_cost": 100.0
        }
        
        self.booking_repo.create.return_value = 1
        booking_id = self.booking_service.create_booking(booking_data)
        self.assertEqual(booking_id, 1)

    def test_create_booking_invalid_dates(self):
        """Test booking service with invalid dates"""
        booking_data = {
            "user_id": 1,
            "vehicle_id": 1,
            "pickup_date": (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%dT%H:%M:%S"),
            "return_date": (datetime.now() + timedelta(days=16)).strftime("%Y-%m-%dT%H:%M:%S"),
            "total_cost": 100.0
        }
        
        with self.assertRaises(ValueError):
            self.booking_service.create_booking(booking_data)

    def test_get_daily_report(self):
        """Test getting a daily report"""
        test_date = datetime.now()
        expected_report = [{"bookings": 5, "total": 500.0}]
        
        self.booking_repo.get_daily_report = Mock(return_value=expected_report)
        
        result = self.booking_service.get_daily_report(test_date)
        
        self.assertEqual(result, expected_report)
        self.booking_repo.get_daily_report.assert_called_once_with(test_date, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)