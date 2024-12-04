
from typing import List, Dict, Optional
from datetime import datetime
from mysql.connector import Error
from database import Database
from models import Vehicle, VehicleStatus
import logging

'''

for logging: for debugging we could use a constant to allow for the debugging testing but 
wouldn't produce in the production environment. 
'''
class VehicleRepository:
    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        file_handler = logging.FileHandler('vehicle_repository.log')
        file_handler.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def create(self, vehicle: Vehicle) -> int:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                INSERT INTO Vehicles (
                    category_id, registration_number, model, 
                    make, year, status, last_maintenance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                vehicle.category_id,
                vehicle.registration_number,
                vehicle.model,
                vehicle.make,
                vehicle.year,
                vehicle.status.value,
                vehicle.last_maintenance
            ))
            return cursor.lastrowid

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM Vehicles 
                WHERE vehicle_id = %s
            """, (vehicle_id,))
            result = cursor.fetchone()
            return Vehicle.from_db_dict(result) if result else None

    def get_available_vehicles(self, start_date: datetime, end_date: datetime,
                            category_id: Optional[int] = None,
                            vehicle_id: Optional[int] = None) -> List[dict]:
        with self.db.get_cursor() as cursor:
            query = """
                SELECT DISTINCT 
                    v.vehicle_id,
                    v.status,
                    v.category_id,
                    v.make,
                    v.model,
                    v.year,
                    v.last_maintenance,
                    vc.daily_rate
                FROM Vehicles v
                INNER JOIN VehicleCategories vc ON v.category_id = vc.category_id
                LEFT JOIN Bookings b ON v.vehicle_id = b.vehicle_id
                WHERE v.status = %s
                AND (b.booking_id IS NULL
                    OR NOT (
                        (b.pickup_date BETWEEN %s AND %s)
                        OR (b.return_date BETWEEN %s AND %s)
                        OR (b.pickup_date <= %s AND b.return_date >= %s)
                    ))
            """
            params = [VehicleStatus.AVAILABLE.name, start_date, end_date, 
                    start_date, end_date, start_date, end_date]
            
            if category_id:
                query += " AND v.category_id = %s"
                params.append(category_id)
            
            if vehicle_id:
                query += " AND v.vehicle_id = %s"
                params.append(vehicle_id)
                    
            cursor.execute(query, tuple(params))
            results = cursor.fetchall()
            return [
                {
                    "vehicle_id": row["vehicle_id"],
                    "status": row["status"],
                    "category_id": row["category_id"],
                    "make": row["make"],
                    "model": row["model"],
                    "year": row["year"],
                    "last_maintenance": row["last_maintenance"],
                    "daily_rate": row["daily_rate"]
                }
                for row in results
            ]





    def update_status(self, vehicle_id: int, status: VehicleStatus) -> None:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE Vehicles 
                SET status = %s 
                WHERE vehicle_id = %s
            """, (status.value, vehicle_id))

    def update_maintenance(self, vehicle_id: int, maintenance_date: datetime) -> None:
        with self.db.get_cursor() as cursor:
            cursor.execute("""
                UPDATE Vehicles 
                SET last_maintenance = %s 
                WHERE vehicle_id = %s
            """, (maintenance_date, vehicle_id))

    def get_daily_report(self, date: datetime, category_id: Optional[int] = None) -> List[Dict]:
        with self.db.get_cursor() as cursor:
            query = """
                SELECT 
                    v.category_id,
                    vc.name as category_name,
                    COUNT(b.booking_id) as booking_count,
                    SUM(b.total_cost) as total_revenue
                FROM Vehicles v
                JOIN VehicleCategories vc ON v.category_id = vc.category_id
                LEFT JOIN Bookings b ON v.vehicle_id = b.vehicle_id
                WHERE DATE(b.pickup_date) = DATE(%s)
                OR DATE(b.return_date) = DATE(%s)
            """
            params = [date, date]

            if category_id:
                query += " AND v.category_id = %s"
                params.append(category_id)

            query += " GROUP BY v.category_id, vc.name"
            
            cursor.execute(query, tuple(params))
            return cursor.fetchall()
