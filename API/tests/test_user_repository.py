import unittest
from unittest.mock import patch
from models import User
from repositories.user_repository import UserRepository

class TestUserRepository(unittest.TestCase):
    def setUp(self):
        """Set up before all tests."""
        self.user_repository = UserRepository()

    @patch('database.Database.get_cursor')
    def test_create_user(self, mock_get_cursor):
        """Test for create user"""
        mock_cursor = mock_get_cursor.return_value.__enter__.return_value
        mock_cursor.lastrowid = 1

        user = User(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            password_hash="temp_hash" 
        )

        created_user_id = self.user_repository.create(user)

        self.assertEqual(created_user_id, 1)
        mock_cursor.execute.assert_called_with(
            "INSERT INTO Users (email, first_name, last_name, password_hash) VALUES (%s, %s, %s, %s)",
            ("test@example.com", "John", "Doe", "temp_hash")
        )

    @patch('database.Database.get_cursor')
    def test_get_user_by_id(self, mock_get_cursor):
        """Test for get user"""
        mock_cursor = mock_get_cursor.return_value.__enter__.return_value
        mock_cursor.fetchone.return_value = {
            "user_id": 1,
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password_hash": "temp_hash",  
            "created_at": None
        }

        user = self.user_repository.get_by_id(1)

        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        mock_cursor.execute.assert_called_with(
            "SELECT user_id, email, first_name, last_name, password_hash, created_at FROM Users WHERE user_id = %s AND is_deleted = FALSE", 
            (1,)
        )

    @patch('database.Database.get_cursor')
    def test_update_user(self, mock_get_cursor):
        """Test for update user"""
        mock_cursor = mock_get_cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        user = User(
            user_id=1,
            email="updated@example.com",
            first_name="Jane",
            last_name="Doe",
            password_hash="temp_hash"  

        updated = self.user_repository.update(user)

        self.assertTrue(updated)
        mock_cursor.execute.assert_called_with(
            "UPDATE Users SET email = %s, first_name = %s, last_name = %s WHERE user_id = %s",
            ("updated@example.com", "Jane", "Doe", 1)
        )

    @patch('database.Database.get_cursor')
    def test_delete_user(self, mock_get_cursor):
        """Test for soft delete user"""
        mock_cursor = mock_get_cursor.return_value.__enter__.return_value
        mock_cursor.rowcount = 1

        deleted = self.user_repository.delete(1)

        self.assertTrue(deleted)
        mock_cursor.execute.assert_called_with(
            "UPDATE Users SET is_deleted = TRUE WHERE user_id = %s", 
            (1,)
        )
        
if __name__ == '__main__':
    unittest.main()