import unittest
from datetime import datetime, timedelta
from repositories.booking_repository import BookingRepository
from models import Booking
from unittest.mock import Mock, patch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBookingRepository(unittest.TestCase):
    def setUp(self):
        """Initialize test environment before each test"""
        self.db_mock = Mock()
        self.cursor_mock = Mock()
        # Create a context manager mock
        context_manager = Mock()
        context_manager.__enter__ = Mock(return_value=self.cursor_mock)
        context_manager.__exit__ = Mock(return_value=None)
        self.db_mock.get_cursor.return_value = context_manager
        
        self.booking_repo = BookingRepository()
        self.booking_repo.db = self.db_mock
    
    def test_create_booking(self):
        """Test creating a new booking"""
        booking = Booking(
            user_id=1,
            vehicle_id=1,
            pickup_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=100.0
        )
        
        self.cursor_mock.lastrowid = 1
        self.cursor_mock.fetchone.return_value = None  # Vehicle is available
        
        booking_id = self.booking_repo.create(booking)
        
        self.assertEqual(booking_id, 1)
        self.cursor_mock.execute.assert_called()  # Verify SQL was executed
   
    def test_vehicle_unavailable(self):
        """Test if previous booked vehicle is no longer available"""
        booking = Booking(
            user_id=1,
            vehicle_id=1,
            pickup_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=100.0
        )
        
        self.cursor_mock.fetchone.return_value = {'id': 1}  # Vehicle is not available
        
        with self.assertRaises(ValueError):
            self.booking_repo.create(booking)

if __name__ == '__main__':
    unittest.main(verbosity=2)