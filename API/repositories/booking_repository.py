
from database import Database
from models import Booking
from mysql.connector import Error
from datetime import datetime
import logging

'''
for logging: for debugging we could use a constant to allow for the debugging testing but 
wouldn't produce in the production environment. 
'''
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
                cursor.execute("SELECT 1 FROM Vehicles WHERE vehicle_id = %s", (booking.vehicle_id,))
                if not cursor.fetchone():
                    raise ValueError(f"Vehicle with ID {booking.vehicle_id} does not exist")

                cursor.execute("SELECT 1 FROM Users WHERE user_id = %s", (booking.user_id,))
                if not cursor.fetchone():
                    raise ValueError(f"User with ID {booking.user_id} does not exist")

                if not self._is_vehicle_available(cursor, booking):
                    self.logger.error("Vehicle not available for selected dates")
                    raise ValueError("Vehicle not available for selected dates")

                cursor.execute("""
                    INSERT INTO Bookings (user_id, vehicle_id, pickup_date, 
                                        return_date, total_cost)
                    VALUES (%s, %s, %s, %s, %s)
                """, (booking.user_id, booking.vehicle_id, booking.pickup_date,
                    booking.return_date, booking.total_cost))
                
                booking_id = cursor.lastrowid

                self._create_invoice(cursor, booking_id, booking.total_cost)
                
                self._log_email(cursor, booking_id, 'confirmation')
                
                cursor.execute("COMMIT")
                return booking_id
            except Error as e:
                cursor.execute("ROLLBACK")
                if e.errno == 1452: 
                    if 'vehicles' in str(e):
                        raise ValueError(f"Vehicle with ID {booking.vehicle_id} does not exist")
                    elif 'users' in str(e):
                        raise ValueError(f"User with ID {booking.user_id} does not exist")
                self.logger.error(f"Database error while creating booking: {e}")
                raise
            except ValueError as e:
                cursor.execute("ROLLBACK")
                self.logger.error(f"Validation error while creating booking: {e}")
                raise
            except Exception as e:
                cursor.execute("ROLLBACK")
                self.logger.error(f"Unexpected error while creating booking: {e}")
                raise

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
        email_type_map = {
            'update': 'confirmation',  
            'confirmation': 'confirmation',
            'invoice': 'invoice',
            'cancelled': 'cancelled'
        }
        
        mapped_type = email_type_map.get(email_type, 'confirmation')
        
        cursor.execute("""
            INSERT INTO EmailLogs (booking_id, email_type)
            VALUES (%s, %s)
        """, (booking_id, mapped_type))

    def update(self, booking_id: int, updated_booking: Booking) -> bool:
        self.logger.info(f"Updating booking: {booking_id}")
        with self.db.get_cursor() as cursor:
            cursor.execute("START TRANSACTION")
            try:
                if self._is_vehicle_available(cursor, updated_booking):
                    self.logger.error("Vehicle not available for updated dates")
                    raise ValueError("Vehicle not available for updated dates")

                cursor.execute("""
                    UPDATE Bookings
                    SET user_id = %s, vehicle_id = %s, pickup_date = %s,
                        return_date = %s, total_cost = %s, status = %s
                    WHERE booking_id = %s
                """, (updated_booking.user_id, updated_booking.vehicle_id,
                      updated_booking.pickup_date, updated_booking.return_date,
                      updated_booking.total_cost, updated_booking.status,
                      booking_id))
                
                if cursor.rowcount == 0:
                    self.logger.error(f"Booking {booking_id} not found")
                    cursor.execute("ROLLBACK")
                    return False

                self._update_invoice(cursor, booking_id, updated_booking.total_cost)
                self._log_email(cursor, booking_id, 'update')
                
                cursor.execute("COMMIT")
                return True
            except Error as e:
                cursor.execute("ROLLBACK")
                raise e
            
    def _update_invoice(self, cursor, booking_id: int, new_amount: float):
        cursor.execute("""
            UPDATE Invoices
            SET amount = %s
            WHERE booking_id = %s
        """, (new_amount, booking_id))

    def delete(self, booking_id: int) -> bool:
        self.logger.info(f"Deleting booking: {booking_id}")
        with self.db.get_cursor() as cursor:
            cursor.execute("START TRANSACTION")
            try:
                cursor.execute("SELECT status FROM Bookings WHERE booking_id = %s", (booking_id,))
                result = cursor.fetchone()
                if not result:
                    self.logger.error(f"Booking {booking_id} not found")
                    return False
                
                # status =  result.get('status') or result[0]
                # status = result[0]
                status = result['status'] if isinstance(result, dict) else result[0]
                
                if status == 'active':
                    self.logger.error(f"Cannot delete active booking {booking_id}")
                    raise ValueError("Cannot delete an active booking")
                
                cursor.execute("UPDATE Bookings SET is_deleted = TRUE WHERE booking_id = %s", (booking_id,))
                cursor.execute("DELETE FROM Invoices WHERE booking_id = %s", (booking_id,))
                self._log_email(cursor, booking_id, 'cancelled')

                cursor.execute("COMMIT")
                self.logger.info(f"Booking {booking_id} soft-deleted successfully")
                return True
            except Error as e:
                cursor.execute("ROLLBACK")
                raise e