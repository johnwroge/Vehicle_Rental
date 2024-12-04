import unittest
from unittest.mock import Mock, patch
from flask import Flask
from routes.user_route import users_api
from services.user_service import UserService
from models import User
from datetime import datetime
import json

class TestUserRoutes(unittest.TestCase):
   def setUp(self):
       """Setup test Flask app and client"""
       self.app = Flask(__name__)
       self.app.register_blueprint(users_api, url_prefix='/api')
       self.client = self.app.test_client()
       
       # Mock user for testing
       self.test_user = User(
           user_id=1,
           email="test@test.com",
           first_name="Test",
           last_name="User",
           password_hash="hash123",
           created_at=datetime.now()
       )

   @patch('routes.user_route.UserService')
   def test_create_user(self, mock_service):
       """Test POST /api/users"""
       # Setup
       mock_service.return_value.create_user.return_value = 1
       test_data = {
           "email": "test@test.com",
           "first_name": "Test",
           "last_name": "User",
           "password_hash": "hash123"
       }

       # Execute
       response = self.client.post(
           '/api/users',
           data=json.dumps(test_data),
           content_type='application/json'
       )

       # Assert
       self.assertEqual(response.status_code, 201)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'success')
       self.assertEqual(data['data']['user_id'], 1)

   @patch('routes.user_route.UserService')
   def test_get_user(self, mock_service):
       """Test GET /api/users/<id>"""
       # Setup
       mock_service.return_value.get_user.return_value = self.test_user

       # Execute
       response = self.client.get('/api/users/1')

       # Assert
       self.assertEqual(response.status_code, 200)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'success')
       self.assertEqual(data['data']['email'], 'test@test.com')

   @patch('routes.user_route.UserService')
   def test_get_nonexistent_user(self, mock_service):
       """Test GET for non-existent user"""
       # Setup
       mock_service.return_value.get_user.return_value = None

       # Execute
       response = self.client.get('/api/users/999')

       # Assert
       self.assertEqual(response.status_code, 404)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'error')
       self.assertEqual(data['message'], 'User not found')

   @patch('routes.user_route.UserService')
   def test_update_user(self, mock_service):
       """Test PUT /api/users/<id>"""
       # Setup
       mock_service.return_value.update_user.return_value = True
       update_data = {
           "email": "updated@test.com",
           "first_name": "Updated",
           "last_name": "User",
           "password_hash": "hash123"
       }

       # Execute
       response = self.client.put(
           '/api/users/1',
           data=json.dumps(update_data),
           content_type='application/json'
       )

       # Assert
       self.assertEqual(response.status_code, 200)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'success')
       self.assertEqual(data['message'], 'User updated successfully')

   @patch('routes.user_route.UserService')
   def test_delete_user(self, mock_service):
       """Test DELETE /api/users/<id>"""
       # Setup
       mock_service.return_value.delete_user.return_value = True

       # Execute
       response = self.client.delete('/api/users/1')

       # Assert
       self.assertEqual(response.status_code, 200)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'success')
       self.assertEqual(data['message'], 'User deleted successfully')

   @patch('routes.user_route.UserService')
   def test_delete_nonexistent_user(self, mock_service):
       """Test DELETE for non-existent user"""
       # Setup
       mock_service.return_value.delete_user.return_value = False

       # Execute
       response = self.client.delete('/api/users/999')

       # Assert
       self.assertEqual(response.status_code, 404)
       data = json.loads(response.data)
       self.assertEqual(data['status'], 'error')
       self.assertEqual(data['message'], 'User not found')

if __name__ == '__main__':
   unittest.main()