import datetime
from models import User, Vehicle, Booking, BookingStatus, VehicleStatus
from repositories import UserRepository, VehicleRepository, BookingRepository


user1 = User(first_name="John", last_name="Doe", email="john@example.com")
user2 = User(first_name="Jane", last_name="Smith", email="jane@example.com")
user_repo = UserRepository()
user1_id = user_repo.create(user1)
user2_id = user_repo.create(user2)


vehicle1 = Vehicle(category_id=1, registration_number="ABC123", model="Toyota Corolla", make="Toyota", year=2020, status=VehicleStatus.AVAILABLE, last_maintenance=datetime.datetime.now())
vehicle2 = Vehicle(category_id=2, registration_number="DEF456", model="Honda Pilot", make="Honda", year=2018, status=VehicleStatus.AVAILABLE, last_maintenance=datetime.datetime.now())
vehicle_repo = VehicleRepository()
vehicle1_id = vehicle_repo.create(vehicle1)
vehicle2_id = vehicle_repo.create(vehicle2)


booking1 = Booking(user_id=user1_id, vehicle_id=vehicle1_id, pickup_date=(datetime.datetime.now() + datetime.timedelta(days=3)).isoformat(), return_date=(datetime.datetime.now() + datetime.timedelta(days=5)).isoformat(), total_cost=100.0, status=BookingStatus.PENDING)
booking2 = Booking(user_id=user2_id, vehicle_id=vehicle2_id, pickup_date=(datetime.datetime.now() + datetime.timedelta(days=7)).isoformat(), return_date=(datetime.datetime.now() + datetime.timedelta(days=10)).isoformat(), total_cost=200.0, status=BookingStatus.PENDING)
booking_repo = BookingRepository()
booking1_id = booking_repo.create(booking1)
booking2_id = booking_repo.create(booking2)