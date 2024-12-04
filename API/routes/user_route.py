from flask import Blueprint, request, jsonify
from services.user_service import UserService
from repositories.user_repository import UserRepository

users_api = Blueprint('users_api', __name__)

@users_api.route('/users', methods=['POST'])
def create_user():
   try:
       user_repo = UserRepository()
       user_service = UserService(user_repo)
       user_id = user_service.create_user(request.json)
       return jsonify({
           'status': 'success',
           'message': 'User created successfully',
           'data': {'user_id': user_id}
       }), 201
   except ValueError as e:
       return jsonify({
           'status': 'error',
           'message': str(e)
       }), 400
   except Exception as e:
       return jsonify({
           'status': 'error',
           'message': 'Internal server error'
       }), 500

@users_api.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_user(user_id):
   try:
       user_repo = UserRepository()
       user_service = UserService(user_repo)

       if request.method == 'GET':
           user = user_service.get_user(user_id)
           if not user:
               return jsonify({
                   'status': 'error',
                   'message': 'User not found'
               }), 404
           return jsonify({
               'status': 'success',
               'data': user.__dict__
           })

       elif request.method == 'PUT':
           if user_service.update_user(user_id, request.json):
               return jsonify({
                   'status': 'success',
                   'message': 'User updated successfully'
               })
           return jsonify({
               'status': 'error',
               'message': 'User not found'
           }), 404

       elif request.method == 'DELETE':
           if user_service.delete_user(user_id):
               return jsonify({
                   'status': 'success',
                   'message': 'User deleted successfully'
               })
           return jsonify({
               'status': 'error',
               'message': 'User not found'
           }), 404

   except ValueError as e:
       return jsonify({
           'status': 'error',
           'message': str(e)
       }), 400
   except Exception as e:
       return jsonify({
           'status': 'error',
           'message': 'Internal server error'
       }), 500