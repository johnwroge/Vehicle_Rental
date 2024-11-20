from flask import Blueprint, request, jsonify, current_app
from services.booking_service import BookingService
from datetime import datetime
from repositories import BookingRepository
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
    
