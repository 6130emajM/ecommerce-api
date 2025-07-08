from flask import Flask
from ecommerce_api.db_setup import db, ma
from ecommerce_api.models import Customer, Order, Product

def create_app():
    app = Flask(__name__)
    
    # Configure your MariaDB URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flaskuser:Indra@localhost/ecommerce_api'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Create DB tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

