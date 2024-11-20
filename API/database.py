import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector import Error
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging

load_dotenv()

class Database:
    _instance = None
    _pool = None

    def __new__(cls):
        logging.info("Database singleton accessed")
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if not cls._pool:
                cls._initialize_pool()
        return cls._instance

    @classmethod
    def _initialize_pool(cls):
        try:
            cls._pool = MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,
                pool_reset_session=True,
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            logging.info("Connection pool initialized successfully.")
        except Error as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    @contextmanager
    def get_cursor(self, dictionary=True):
        conn = None
        cursor = None
        try:
            conn = self._pool.get_connection()
            cursor = conn.cursor(dictionary=dictionary)
            yield cursor
            conn.commit()
        except Error as e:
            if conn:
                conn.rollback()
            logging.error(f"Database error: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def test_connection(self):
        try:
            with self.get_cursor() as cursor:
                cursor.execute("SELECT 1")
                return True
        except Error as e:
            logging.error(f"Connection pool test failed: {e}")
            return False