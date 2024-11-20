import unittest
from database import Database
from mysql.connector import Error
import logging

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up before all tests."""
        logging.basicConfig(level=logging.INFO)
        cls.db = Database()  

    def test_connection_pool(self):
        """Test that connection pool is initialized."""
        self.assertIsNotNone(self.db._pool)

    def test_get_cursor(self):
        """Test the get_cursor method."""
        try:
            with self.db.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                self.assertEqual(result.get('1'), 1)
        except Error as e:
            self.fail(f"Database error occurred: {e}")

    def test_multiple_connections(self):
        """Test multiple simultaneous connections."""
        try:
            connections = []
            for _ in range(3):  
                with self.db.get_cursor() as cursor:
                    cursor.execute("SELECT CONNECTION_ID()")
                    connection_id = cursor.fetchone()
                    connections.append(connection_id.get('CONNECTION_ID()'))
            
            self.assertEqual(len(set(connections)), 3)
        except Error as e:
            self.fail(f"Database error occurred: {e}")

    def test_get_cursor_with_error(self):
        """Test handling of an error in get_cursor."""
        with self.assertRaises(Error):
            with self.db.get_cursor() as cursor:
                cursor.execute("SELECT * FROM non_existing_table")

if __name__ == "__main__":
    unittest.main()