import unittest
from unittest.mock import Mock
from services.user_service import UserService
from models import User
from datetime import datetime

class TestUserService(unittest.TestCase):
    def setUp(self):
        """Setup test environment"""
        self.mock_repo = Mock()
        self.user_service = UserService(self.mock_repo)
        self.test_user_data = {
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "password_hash": "hash123"
        }

    def test_create_user(self):
        """Test user creation through service"""
        # Setup
        self.mock_repo.create.return_value = 1

        # Execute
        user_id = self.user_service.create_user(self.test_user_data)

        # Assert
        self.assertEqual(user_id, 1)
        self.mock_repo.create.assert_called_once()

    def test_get_user(self):
        """Test getting user through service"""
        # Setup
        mock_user = User(
            user_id=1,
            email="test@test.com",
            first_name="Test",
            last_name="User",
            password_hash="hash123",
            created_at=datetime.now()
        )
        self.mock_repo.get_by_id.return_value = mock_user

        # Execute
        user = self.user_service.get_user(1)

        # Assert
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "test@test.com")
        self.mock_repo.get_by_id.assert_called_once_with(1)

    def test_update_user(self):
        """Test updating user through service"""
        # Setup
        self.mock_repo.update.return_value = True
        update_data = {
            "email": "updated@test.com",
            "first_name": "Updated",
            "last_name": "User",
            "password_hash": "hash123"
        }

        # Execute
        success = self.user_service.update_user(1, update_data)

        # Assert
        self.assertTrue(success)
        self.mock_repo.update.assert_called_once()

    def test_delete_user(self):
        """Test deleting user through service"""
        # Setup
        self.mock_repo.delete.return_value = True

        # Execute
        success = self.user_service.delete_user(1)

        # Assert
        self.assertTrue(success)
        self.mock_repo.delete.assert_called_once_with(1)

    def test_get_nonexistent_user(self):
        """Test getting a non-existent user returns None"""
        # Setup
        self.mock_repo.get_by_id.return_value = None

        # Execute
        user = self.user_service.get_user(999)

        # Assert
        self.assertIsNone(user)
        self.mock_repo.get_by_id.assert_called_once_with(999)

if __name__ == '__main__':
    unittest.main()