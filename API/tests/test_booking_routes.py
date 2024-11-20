import unittest
from datetime import datetime, timedelta
from flask import Flask
from routes.booking_route import bookings_api
from services.booking_service import BookingService
from unittest.mock import Mock, patch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestBookingRoutes(unittest.TestCase):
    def setUp(self):
        """Initialize test environment before each test"""
        self.app = Flask(__name__)
        self.app.register_blueprint(bookings_api, url_prefix='/api')
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        self.mock_service = Mock(spec=BookingService)
        self.patcher = patch('routes.booking_route.BookingService', return_value=self.mock_service)
        self.patcher.start()
        logger.info("Test setup completed")

    def tearDown(self):
        """Clean up after each test"""
        self.patcher.stop()
        logger.info("Test teardown completed")

    def test_create_booking_success(self):
        """Test successful booking creation"""
        self.mock_service.create_booking.return_value = 1
        
        booking_data = {
            "user_id": 1,
            "vehicle_id": 1,
            "pickup_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "return_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "total_cost": 100.0
        }

        response = self.client.post('/api/bookings', json=booking_data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"booking_id": 1})
        self.mock_service.create_booking.assert_called_once_with(booking_data)
        logger.info("Successful booking creation test completed")

    def test_create_booking_invalid_data(self):
        """Test booking creation with invalid data"""
        self.mock_service.create_booking.side_effect = ValueError("Invalid booking data")
        
        invalid_data = {
            "user_id": 1,
        }
        
        response = self.client.post('/api/bookings', json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid booking data"})
        logger.info("Invalid booking data test completed")

    def test_create_booking_service_error(self):
        """Test booking creation with service error"""
        self.mock_service.create_booking.side_effect = ValueError("Vehicle not available")
        
        booking_data = {
            "user_id": 1,
            "vehicle_id": 1,
            "pickup_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            "return_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M:%S"),
            "total_cost": 100.0
        }
        
        response = self.client.post('/api/bookings', json=booking_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["error"], "Vehicle not available")
        logger.info("Service error test completed")

    # def test_get_bookings(self):
    #     """Test get bookings endpoint"""
    #     response = self.client.get('/api/bookings')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data.decode(), 'Success')
    #     logger.info("Get bookings test completed")

if __name__ == '__main__':
    unittest.main(verbosity=2)