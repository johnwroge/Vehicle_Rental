from flask import Blueprint, request, jsonify
from services import VehicleService
from datetime import datetime
from repositories import BookingRepository, VehicleRepository

vehicles_api = Blueprint('vehicles_api', __name__)

@vehicles_api.route('/vehicles/availability', methods=['GET'])
def check_availability():
    try:
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        category_id = request.args.get('category_id')
        vehicle_id = request.args.get('vehicle_id')

        vehicle_repo = VehicleRepository()
        vehicle_service = VehicleService(vehicle_repo)
        vehicles = vehicle_service._is_vehicle_available(
            start_date, end_date, category_id, vehicle_id
        )
        return jsonify(vehicles)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    