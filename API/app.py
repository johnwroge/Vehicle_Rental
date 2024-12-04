from flask import Flask
from database import Database 
import logging
from routes import api  
# from flasgger import Swagger

logging.basicConfig(level=logging.INFO)
db = Database()

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = db

#     app.config['SWAGGER'] = {
#     'title': 'Vehicle Rental API',
#     'version': '1.0',
#     'description': 'API for managing vehicle rentals'
#     }
#    Swagger(app)

    for blueprint in api:
        app.register_blueprint(blueprint, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)