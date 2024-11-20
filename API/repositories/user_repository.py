
from database import Database
from models import User, Vehicle, Booking
from typing import List, Optional
from mysql.connector import Error

class UserRepository:
    def __init__(self):
        self.db = Database()

    def create(self, user: User) -> int:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO Users (email, first_name, last_name, password_hash)
                VALUES (%s, %s, %s, %s)
            """, (user.email, user.first_name, user.last_name, 'temp_hash'))
            return cursor.lastrowid

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            data = cursor.fetchone()
            return User.from_db_dict(data) if data else None

    def update(self, user: User) -> bool:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE Users 
                SET email = %s, first_name = %s, last_name = %s
                WHERE user_id = %s
            """, (user.email, user.first_name, user.last_name, user.user_id))
            return cursor.rowcount > 0