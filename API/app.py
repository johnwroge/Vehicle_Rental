
from flask import Flask
from database import Database 
import logging

logging.basicConfig(level=logging.INFO)

db = Database()

def create_app():
    app = Flask(__name__)  

    app.config['DATABASE'] = db 

    # @app.route('/db-test')
    # def db_test():  
    #     try:
    #         with app.config['DATABASE'].get_cursor() as cursor:
    #             cursor.execute("SHOW TABLES")
    #             tables = cursor.fetchall()
    #             return f"Database connected. Tables: {tables}"
    #     except Exception as e:
    #         return f"Database connection error: {str(e)}"

    return app
 
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)