from flask import Blueprint, request, jsonify, current_app
from services.booking_service import BookingService
from datetime import datetime
from repositories import BookingRepository
from repositories.vehicle_repository import VehicleRepository
from database import Database

bookings_api = Blueprint('bookings_api', __name__)

@bookings_api.route('/bookings', methods=['POST'])
def create_booking():
    try:
        booking_repo = BookingRepository()
        booking_service = BookingService(booking_repo)
        booking_id = booking_service.create_booking(request.json)
        return jsonify({'booking_id': booking_id}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        
        current_app.logger.error(f"Error occurred while creating booking: {e}", exc_info=True)
        
        return jsonify({
            'error': 'An unexpected error occurred while processing your booking request. Please try again later.',
            'details': str(e)
        }), 500

@bookings_api.route('/daily_report', methods=['GET'])
def get_daily_report():
    date_str = request.args.get('date')
    category_id = request.args.get('category_id', type=int)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    vehicle_repo = VehicleRepository()
    report = vehicle_repo.get_daily_report(date, category_id)

    return jsonify(report), 200
    
