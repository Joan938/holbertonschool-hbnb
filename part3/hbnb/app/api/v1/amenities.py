from flask_restx import Namespace, Resource, fields
from app.services import facade
""" API endpoints for amenities """

api = Namespace('amenities', description='Amenity operations')
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route("/")
class AmenityList(Resource):
    """Resource for creating and retrieving amenities"""
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201
        except Exception as e:
            return {'error': str(e)}, 400
    
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get all amenities"""
        try:
            # FIXED: Use facade method instead of direct repo access
            amenities = facade.get_all_amenities()
            if not amenities:
                return {"message": "No amenities found"}, 200  # Changed from 404 to 200
            return [
                {
                    'id': amenity.id,
                    'name': amenity.name
                }
                for amenity in amenities
            ], 200
        except Exception as e:
            return {'error': str(e)}, 500

@api.route("/<amenity_id>")
class AmenityResource(Resource):
    """Resource for getting, updating and deleting amenity details"""
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            return {
                'id': amenity.id,
                'name': amenity.name
            }, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": "Amenity not found"}, 404
            
            updated_details = api.payload
            updated_amenity = facade.update_amenity(amenity_id, updated_details)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200
        except Exception as e:
            return {'error': str(e)}, 400