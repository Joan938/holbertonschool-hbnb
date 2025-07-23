from flask import Blueprint
from flask_restx import Api

bp = Blueprint('api', __name__)
api = Api(bp, title='HBnB API', version='1.0', description='HBnB REST API')

from .users import ns as users_ns
from .auth import ns as auth_ns

api.add_namespace(auth_ns, path='/auth')
api.add_namespace(users_ns, path='/users')