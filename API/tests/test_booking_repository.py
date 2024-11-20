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
        self.cursor_mock.fetchone.return_value = None  
        
        booking_id = self.booking_repo.create(booking)
        
        self.assertEqual(booking_id, 1)
        self.cursor_mock.execute.assert_called() 
   
    def test_vehicle_unavailable(self):
        """Test if previous booked vehicle is no longer available"""
        booking = Booking(
            user_id=1,
            vehicle_id=1,
            pickup_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=100.0
        )
        
        self.cursor_mock.fetchone.return_value = {'id': 1}  
        
        with self.assertRaises(ValueError):
            self.booking_repo.create(booking)
    
    def test_update_booking(self):
        """Test updating an existing booking"""
        booking = Booking(
            user_id=1,
            vehicle_id=1,
            pickup_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=150.0,
            status='pending'
        )
        
        self.cursor_mock.fetchone.return_value = None 
        self.cursor_mock.rowcount = 1 
        
        result = self.booking_repo.update(1, booking)
        
        self.assertTrue(result)
        self.cursor_mock.execute.assert_called()

    def test_update_booking_vehicle_unavailable(self):
        """Test updating a booking when the vehicle becomes unavailable"""
        booking = Booking(
            user_id=1,
            vehicle_id=1,
            pickup_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            return_date=(datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            total_cost=150.0,
            status='pending'
        )
        
        self.cursor_mock.fetchone.return_value = {'id': 1} 
        
        with self.assertRaises(ValueError):
            self.booking_repo.update(1, booking)

    def test_delete_booking(self):
        """Test deleting a booking"""
        self.cursor_mock.fetchone.return_value = ('pending',)  
        
        result = self.booking_repo.delete(1)
        
        self.assertTrue(result)
        self.cursor_mock.execute.assert_called()  

    def test_delete_active_booking(self):
        """Test deleting an active booking (should raise ValueError)"""
        self.cursor_mock.fetchone.return_value = ('active',) 
        
        with self.assertRaises(ValueError):
            self.booking_repo.delete(1)

    def test_delete_nonexistent_booking(self):
        """Test deleting a booking that doesn't exist"""
        self.cursor_mock.fetchone.return_value = None 
        
        result = self.booking_repo.delete(1)
        
        self.assertFalse(result)  
    
    

if __name__ == '__main__':
    unittest.main(verbosity=2)