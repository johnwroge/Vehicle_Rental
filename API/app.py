from flask import Flask
from database import Database 
import logging
from routes import api  

logging.basicConfig(level=logging.INFO)
db = Database()

def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = db

    for blueprint in api:
        app.register_blueprint(blueprint, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)