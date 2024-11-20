
from database import Database
from models import User, Vehicle, Booking
from typing import List, Optional
from mysql.connector import Error
import logging

class UserRepository:
    def __init__(self):
        self.db = Database()
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler('user_repository.log')
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def create(self, user: User) -> int:
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "INSERT INTO Users (email, first_name, last_name, password_hash) "
                "VALUES (%s, %s, %s, %s)",
                (user.email, user.first_name, user.last_name, 'temp_hash')
            )
            return cursor.lastrowid

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            data = cursor.fetchone()
            return User.from_db_dict(data) if data else None

    def update(self, user: User) -> bool:
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "UPDATE Users "
                "SET email = %s, first_name = %s, last_name = %s "
                "WHERE user_id = %s",
                (user.email, user.first_name, user.last_name, user.user_id)
            )
            return cursor.rowcount > 0
        
    def delete(self, user_id: int) -> bool:
        with self.db.get_cursor() as cursor:
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            return cursor.rowcount > 0