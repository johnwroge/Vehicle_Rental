
import datetime
import random
from models import User, Vehicle, VehicleStatus
from repositories import UserRepository, VehicleRepository

def generate_users_and_vehicles():
    user_repo = UserRepository()
    vehicle_repo = VehicleRepository()
    created_users = []
    created_vehicles = []

    for i in range(10):  
        first_name = f"User{i+1}"
        last_name = f"Test{i+1}"
        email = f"user{i+1}@example.com"
        
        user = User(first_name=first_name, last_name=last_name, email=email)
        user_id = user_repo.create(user)
        created_users.append((user_id, user))

    makes = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan"]
    models = ["Sedan", "SUV", "Truck", "Compact", "Luxury"]
    current_year = datetime.datetime.now().year

    for i in range(15):  
        make = makes[i % len(makes)]
        model = models[i % len(models)]
        year = random.randint(current_year - 5, current_year)
        registration_number = f"REG-{1000 + i}"
        category_id = (i % 3) + 1 
        
        vehicle = Vehicle(
            category_id=category_id,
            registration_number=registration_number,
            model=f"{make} {model}",
            make=make,
            year=year,
            status=VehicleStatus.AVAILABLE,
            last_maintenance=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))
        )
        vehicle_id = vehicle_repo.create(vehicle)
        created_vehicles.append((vehicle_id, vehicle))

    return created_users, created_vehicles

users, vehicles = generate_users_and_vehicles()


print("Created Users:")
for user_id, user in users:
    print(f"ID: {user_id}, Name: {user.first_name} {user.last_name}, Email: {user.email}")

print("\nCreated Vehicles:")
for vehicle_id, vehicle in vehicles:
    print(f"ID: {vehicle_id}, Vehicle: {vehicle.make} {vehicle.model}, Year: {vehicle.year}, Reg: {vehicle.registration_number}")

