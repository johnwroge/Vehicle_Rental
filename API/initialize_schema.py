import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_schema():
    conn = None
    try:
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        database_name = os.getenv('DB_NAME', 'vehicle_rental')

        cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cursor.execute(f"CREATE DATABASE {database_name}")
        
        cursor.execute(f"USE {database_name}")

        with open('schema.sql', 'r') as f:
            schema_script = f.read()

        statements = [stmt.strip() for stmt in schema_script.split(';') if stmt.strip()]

        statements = [stmt for stmt in statements if not stmt.startswith(('CREATE DATABASE', 'USE'))]

        for statement in statements:
            try:
                cursor.execute(statement)
            except Error as stmt_error:
                print(f"Error in statement: {statement}")
                print(f"Error details: {stmt_error}")
                raise

        conn.commit()
        print(f"Database {database_name} created and schema initialized successfully.")

    except Error as e:
        print(f"Error initializing schema: {e}")
        if conn:
            conn.rollback()
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    initialize_schema()