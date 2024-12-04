from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    password_hash: str
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.created_at = self.created_at or datetime.now()

    @classmethod
    def from_db_dict(cls, data: Dict) -> 'User':
        return cls(**data)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"