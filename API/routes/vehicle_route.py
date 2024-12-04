from flask import Blueprint, request, jsonify
from services import VehicleService
from datetime import datetime
from repositories import VehicleRepository

vehicles_api = Blueprint('vehicles_api', __name__)

'''
"""
http://127.0.0.1:5000/api/vehicles/availability

should be using params, and use a conditional. 
user input validation can also be used. if not receiving fields 40x back to user 
saying we need those fields. In documentation, should also show this in api documentation
so they can expect those errors. Need to get pedantic. The user needs the feedback. 
"""
'''

@vehicles_api.route('/vehicles/availability', methods=['GET'])
def check_availability():
    try:
        # Check required fields
        required_fields = ['start_date', 'end_date']
        missing_fields = [field for field in required_fields if not request.args.get(field)]
        if missing_fields:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields',
                'details': f"Missing: {', '.join(missing_fields)}"
            }), 400

        # Parse dates
        try:
            start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
            end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid date format',
                'details': 'Dates must be in YYYY-MM-DD format'
            }), 400

        # Optional fields
        category_id = int(request.args.get('category_id')) if request.args.get('category_id') else None
        vehicle_id = int(request.args.get('vehicle_id')) if request.args.get('vehicle_id') else None

        vehicle_repo = VehicleRepository()
        vehicle_service = VehicleService(vehicle_repo)
        vehicles = vehicle_service.check_availability(  # Changed method name
            start_date, end_date, category_id, vehicle_id
        )
        
        return jsonify({
            'status': 'success',
            'data': vehicles
        })

    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'details': str(e)
        }), 500