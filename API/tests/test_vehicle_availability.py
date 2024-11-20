import unittest
from datetime import datetime, timedelta
from services.vehicle_service import VehicleService
from repositories.vehicle_repository import VehicleRepository
from unittest.mock import Mock

class TestVehicleService(unittest.TestCase):
    def setUp(self):
        self.vehicle_repo = Mock(spec=VehicleRepository)
        self.vehicle_service = VehicleService(self.vehicle_repo)

    def test_check_availability_by_category(self):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=3)
        category_id = 1
        mock_vehicles = [
            {'vehicle_id': 1, 'status': 'available'},
            {'vehicle_id': 2, 'status': 'available'}
        ]

        self.vehicle_repo.get_available_vehicles.return_value = mock_vehicles
        result = self.vehicle_service.check_availability(
            start_date=start_date,
            end_date=end_date,
            category_id=category_id
        )

        self.assertEqual(len(result), 2)
        self.vehicle_repo.get_available_vehicles.assert_called_with(
            start_date, end_date, category_id, None
        )

    def test_check_availability_specific_vehicle(self):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=3)
        vehicle_id = 1
        mock_result = [{'vehicle_id': 1, 'status': 'available'}]

        self.vehicle_repo.get_available_vehicles.return_value = mock_result
        result = self.vehicle_service.check_availability(
            start_date=start_date,
            end_date=end_date,
            vehicle_id=vehicle_id
        )

        self.assertEqual(len(result), 1)
        self.vehicle_repo.get_available_vehicles.assert_called_with(
            start_date, end_date, None, vehicle_id
        )

    def test_check_availability_no_results(self):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=3)

        self.vehicle_repo.get_available_vehicles.return_value = []
        result = self.vehicle_service.check_availability(start_date, end_date)

        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()