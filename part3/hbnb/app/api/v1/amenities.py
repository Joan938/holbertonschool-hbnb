# hbnb/app/api/v1/amenities.py
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route("/")
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new amenity (admin only)"""
        current = get_jwt_identity()
        if not current.get('is_admin'):
            return {'error': 'Admins only'}, 403

        a = facade.create_amenity(api.payload)
        return {'id': a.id, 'name': a.name}, 201

    @jwt_required()
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """List all amenities"""
        lst = facade.get_all_amenities()
        return [{'id': a.id, 'name': a.name} for a in lst], 200

@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @jwt_required()
    @api.response(200, 'Amenity retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        a = facade.get_amenity(amenity_id)
        if not a:
            return {'error': 'Amenity not found'}, 404
        return {'id': a.id, 'name': a.name}, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity (admin only)"""
        current = get_jwt_identity()
        if not current.get('is_admin'):
            return {'error': 'Admins only'}, 403

        a = facade.update_amenity(amenity_id, api.payload)
        if not a:
            return {'error': 'Amenity not found'}, 404
        return {'id': a.id, 'name': a.name}, 200

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        current = get_jwt_identity()
        if not current.get('is_admin'):
            return {'error': 'Admins only'}, 403

        ok = facade.delete_amenity(amenity_id)
        if not ok:
            return {'error': 'Amenity not found'}, 404
        return {'message': 'Amenity deleted successfully'}, 200
