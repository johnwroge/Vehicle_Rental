
from typing import List, Dict, Optional
from datetime import datetime
from repositories.vehicle_repository import VehicleRepository

class VehicleService:
    def __init__(self, vehicle_repo: VehicleRepository):
        self.vehicle_repo = vehicle_repo

    def check_availability(self, start_date: datetime, end_date: datetime,
                           category_id: Optional[int] = None,
                           vehicle_id: Optional[int] = None) -> List[Dict]:
        return self.vehicle_repo.get_available_vehicles(start_date, end_date, category_id, vehicle_id)