
from database import Database
from models import User, Vehicle, Booking
from typing import List, Optional
from mysql.connector import Error
from datetime import datetime
import logging

class BookingRepository:
    def __init__(self):
        self.db = Database()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler('booking_repository.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def create(self, booking: Booking) -> int:
        self.logger.info(f"Creating new booking: {booking}")
        with self.db.get_cursor() as cursor:
 
            cursor.execute("START TRANSACTION")
            try:
                if not self._is_vehicle_available(cursor, booking):
                    self.logger.error("Vehicle not available for selected dates")
                    raise ValueError("Vehicle not available for selected dates")

                cursor.execute("""
                    INSERT INTO Bookings (user_id, vehicle_id, pickup_date, 
                                        return_date, total_cost, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (booking.user_id, booking.vehicle_id, booking.pickup_date,
                      booking.return_date, booking.total_cost, booking.status.value))
                
                booking_id = cursor.lastrowid

                self._create_invoice(cursor, booking_id, booking.total_cost)
                
                self._log_email(cursor, booking_id, 'confirmation')
                
                cursor.execute("COMMIT")
                return booking_id
            except Error as e:
                cursor.execute("ROLLBACK")
                raise e

    def _is_vehicle_available(self, cursor, booking: Booking) -> bool:
        cursor.execute("""
            SELECT 1 FROM Bookings
            WHERE vehicle_id = %s
            AND status IN ('pending', 'active')
            AND (
                (pickup_date BETWEEN %s AND %s)
                OR (return_date BETWEEN %s AND %s)
                OR (pickup_date <= %s AND return_date >= %s)
            )
        """, (booking.vehicle_id, booking.pickup_date, booking.return_date,
              booking.pickup_date, booking.return_date, booking.pickup_date,
              booking.return_date))
        
        return cursor.fetchone() is None

    def _create_invoice(self, cursor, booking_id: int, amount: float):
        invoice_number = f"INV-{booking_id}-{datetime.now().strftime('%Y%m%d')}"
        cursor.execute("""
            INSERT INTO Invoices (booking_id, amount, invoice_number)
            VALUES (%s, %s, %s)
        """, (booking_id, amount, invoice_number))

    def _log_email(self, cursor, booking_id: int, email_type: str):
        cursor.execute("""
            INSERT INTO EmailLogs (booking_id, email_type)
            VALUES (%s, %s)
        """, (booking_id, email_type))