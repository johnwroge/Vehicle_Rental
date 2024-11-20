from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
from .enums import VehicleStatus

@dataclass
class Vehicle:
    category_id: int
    registration_number: str
    model: str
    make: str
    year: int
    status: VehicleStatus = VehicleStatus.AVAILABLE
    vehicle_id: Optional[int] = None
    last_maintenance: Optional[datetime] = None

    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = VehicleStatus(self.status)

    def needs_maintenance(self, maintenance_interval_days: int = 30) -> bool:
        if not self.last_maintenance:
            return True
        return (datetime.now() - self.last_maintenance).days >= maintenance_interval_days

    @classmethod
    def from_db_dict(cls, data: Dict) -> 'Vehicle':
        return cls(**data)