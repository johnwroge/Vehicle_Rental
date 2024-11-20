import unittest
from datetime import datetime, timedelta
from repositories.vehicle_repository import VehicleRepository
from models import Vehicle, VehicleStatus
from unittest.mock import Mock

class TestVehicleRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.cursor_mock = Mock()
        context_manager = Mock()
        context_manager.__enter__ = Mock(return_value=self.cursor_mock)
        context_manager.__exit__ = Mock(return_value=None)
        self.db_mock.get_cursor.return_value = context_manager
        
        self.vehicle_repo = VehicleRepository()
        self.vehicle_repo.db = self.db_mock

        self.test_vehicle = Vehicle(
            category_id=1,
            registration_number="ABC123",
            model="Camry",
            make="Toyota",
            year=2024,
            status=VehicleStatus.AVAILABLE
        )

    def test_create_vehicle(self):
        self.cursor_mock.lastrowid = 1
        vehicle_id = self.vehicle_repo.create(self.test_vehicle)
        self.assertEqual(vehicle_id, 1)
        self.cursor_mock.execute.assert_called_once()

    def test_get_by_id(self):
        vehicle_data = {
            'vehicle_id': 1,
            'category_id': 1,
            'registration_number': 'ABC123',
            'model': 'Camry',
            'make': 'Toyota',
            'year': 2024,
            'status': 'available',
            'last_maintenance': None
        }
        self.cursor_mock.fetchone.return_value = vehicle_data
        
        vehicle = self.vehicle_repo.get_by_id(1)
        self.assertIsNotNone(vehicle)
        self.assertEqual(vehicle.registration_number, 'ABC123')

    def test_get_by_id_not_found(self):
        self.cursor_mock.fetchone.return_value = None
        vehicle = self.vehicle_repo.get_by_id(999)
        self.assertIsNone(vehicle)

    def test_get_available_vehicles(self):
        vehicles_data = [
            {
                'vehicle_id': 1,
                'category_id': 1,
                'registration_number': 'ABC123',
                'model': 'Camry',
                'make': 'Toyota',
                'year': 2024,
                'status': 'available',
                'last_maintenance': None
            },
            {
                'vehicle_id': 2,
                'category_id': 1,
                'registration_number': 'XYZ789',
                'model': 'Corolla',
                'make': 'Toyota',
                'year': 2024,
                'status': 'available',
                'last_maintenance': None
            }
        ]
        self.cursor_mock.fetchall.return_value = vehicles_data
        
        vehicles = self.vehicle_repo.get_available_vehicles()
        self.assertEqual(len(vehicles), 2)
        self.assertEqual(vehicles[0].status, VehicleStatus.AVAILABLE)

    def test_get_available_vehicles_by_category(self):
        # Mock data that matches your vehicle model
        mock_results = [{
            'vehicle_id': 1,
            'category_id': 1,
            'registration_number': 'ABC123',
            'model': 'Camry',
            'make': 'Toyota',
            'year': 2024,
            'status': 'available',
            'last_maintenance': None
        }]
        self.cursor_mock.fetchall.return_value = mock_results
        
        vehicles = self.vehicle_repo.get_available_vehicles(category_id=1)
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].registration_number, 'ABC123')

    def test_update_status(self):
        self.vehicle_repo.update_status(1, VehicleStatus.RENTED)
        self.cursor_mock.execute.assert_called_once()
        # Verify status was updated to 'rented'
        call_args = self.cursor_mock.execute.call_args[0]
        self.assertEqual(call_args[1][0], 'rented')

    def test_update_maintenance(self):
        maintenance_date = datetime.now()
        self.vehicle_repo.update_maintenance(1, maintenance_date)
        self.cursor_mock.execute.assert_called_once()
        # Verify maintenance date was updated
        call_args = self.cursor_mock.execute.call_args[0]
        self.assertEqual(call_args[1][0], maintenance_date)

    def test_get_daily_report(self):
        report_data = [{
            'category_id': 1,
            'category_name': 'Small Car',
            'booking_count': 5,
            'total_revenue': 500.00
        }]
        self.cursor_mock.fetchall.return_value = report_data
        
        report = self.vehicle_repo.get_daily_report(datetime.now())
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]['booking_count'], 5)

    def test_get_daily_report_with_category(self):
        test_date = datetime.now()
        self.vehicle_repo.get_daily_report(test_date, category_id=1)
        self.cursor_mock.execute.assert_called_once()
        # Verify category filter was applied
        call_args = self.cursor_mock.execute.call_args[0]
        self.assertIn("category_id = %s", call_args[0])

if __name__ == '__main__':
    unittest.main()
