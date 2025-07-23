from flask import Flask
from flask_restx import Api  # type: ignore
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import config

# instantiate extensions
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

# import namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns

def create_app(config_name: str = 'default') -> Flask:
    """
    Application factory: creates and configures the Flask app.
    """
    app = Flask(__name__)
    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Create all tables
    with app.app_context():
        db.create_all()

    # Initialize API
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Register namespaces
    api.add_namespace(auth_ns,      path='/api/v1/auth')
    api.add_namespace(users_ns,     path='/api/v1/users')
    api.add_namespace(places_ns,    path='/api/v1/places')
    api.add_namespace(reviews_ns,   path='/api/v1/reviews')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')

    return app