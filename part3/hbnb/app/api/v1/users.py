# hbnb/app/api/v1/users.py

from flask_restx import Namespace, Resource, fields  # type: ignore
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name':  fields.String(required=True, description='Last name of the user'),
    'email':      fields.String(required=True, description='Email of the user'),
    'password':   fields.String(required=True, description='Password (min 8 chars)', min_length=8)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'message': 'User created successfully'}, 201
        except (ValueError, TypeError, AssertionError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully')
    @api.response(404, 'No users found')
    def get(self):
        """Retrieve all users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404

        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            } for u in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update a user's information"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        updated_data = api.payload.copy()
        updated_data.pop('password', None)  # disallow password changes here
        try:
            updated_user = facade.update_user(user_id, updated_data)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except (ValueError, TypeError, AssertionError) as e:
            return {'error': str(e)}, 400
