from flask import Blueprint, request, jsonify, current_app
from services.booking_service import BookingService
from datetime import datetime
from repositories import BookingRepository
from repositories.vehicle_repository import VehicleRepository
from mysql.connector import Error as MySQLError

bookings_api = Blueprint('bookings_api', __name__)

@bookings_api.route('/bookings', methods=['POST'])
def create_booking():
    try:
        booking_repo = BookingRepository()
        booking_service = BookingService(booking_repo)
        booking_id = booking_service.create_booking(request.json)
        return jsonify({'booking_id': booking_id}), 201
    except MySQLError as e:
        error_code = e.errno
        if error_code == 1452: 
            if 'vehicles' in str(e):
                return jsonify({
                    'error': 'Invalid Vehicle',
                    'details': 'The specified vehicle does not exist in the database.'
                }), 400
            elif 'users' in str(e):
                return jsonify({
                    'error': 'Invalid User',
                    'details': 'The specified user does not exist in the database.'
                }), 400
            else:
                return jsonify({
                    'error': 'Foreign Key Constraint Violation',
                    'details': 'A referenced record does not exist.'
                }), 400
        elif error_code == 1062:  
            return jsonify({
                'error': 'Duplicate Entry',
                'details': 'A booking with these details already exists.'
            }), 400
        else:
            current_app.logger.error(f"Database error: {e}", exc_info=True)
            return jsonify({
                'error': 'Database Error',
                'details': f"An error occurred while processing your request. Error code: {error_code}"
            }), 500
    except Exception as e:
        current_app.logger.error(f"Error occurred while creating booking: {e}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred while processing your booking request.',
            'details': str(e)
        }), 500

@bookings_api.route('/bookings/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    try:
        booking_repo = BookingRepository()
        booking_service = BookingService(booking_repo)
        updated = booking_service.update_booking(booking_id, request.json)
        if updated:
            return jsonify({'message': 'Booking updated successfully'}), 200
        return jsonify({'error': 'Booking not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error occurred while updating booking: {e}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred while processing your update request. Please try again later.',
            'details': str(e)
        }), 500

@bookings_api.route('/bookings/<int:booking_id>', methods=['DELETE'])
def delete_booking(booking_id):
    try:
        booking_repo = BookingRepository()
        booking_service = BookingService(booking_repo)
        deleted = booking_service.delete_booking(booking_id)
        if deleted:
            return jsonify({'message': 'Booking deleted successfully'}), 200
        return jsonify({'error': 'Booking not found'}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error occurred while deleting booking: {e}", exc_info=True)
        return jsonify({
            'error': 'An unexpected error occurred while processing your delete request. Please try again later.',
            'details': str(e)
        }), 500

'''

should be using params, and use a conditional. 
user input validation can also be used. if not receiving fields 40x back to user 
saying we need those fields. In documentation, should also show this in api documentation
so they can expect those errors. Need to get pedantic. The user needs the feedback. 
'''

@bookings_api.route('/daily_report', methods=['GET'])
def get_daily_report():
    date_str = request.args.get('date')
    category_id = request.args.get('category_id', type=int)
    # this is the correct approach, try-catch for sanity checks. 
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    vehicle_repo = VehicleRepository()
    report = vehicle_repo.get_daily_report(date, category_id)

    return jsonify(report), 200
    
