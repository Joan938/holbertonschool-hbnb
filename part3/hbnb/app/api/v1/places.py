from flask_restx import Namespace, Resource, fields  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

amenity_model = api.model('PlaceAmenity', {'id': fields.String(), 'name': fields.String()})
user_model    = api.model('PlaceUser',    {'id': fields.String(), 'first_name': fields.String(), 'last_name': fields.String(), 'email': fields.String()})

place_model = api.model('Place', {
    'title':      fields.String(required=True),
    'description':fields.String,
    'price':      fields.Float(required=True),
    'latitude':   fields.Float(required=True),
    'longitude':  fields.Float(required=True),
    'owner':      fields.Nested(user_model),
    'amenities':  fields.List(fields.String)
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new place (Authentication required)"""
        current_user = get_jwt_identity()
        data = api.payload.copy()
        
        # Set the owner_id to the authenticated user
        data['owner_id'] = current_user
        
        try:
            place = facade.create_place(data)
            return {
                'id': place.id, 
                'title': place.title, 
                'description': place.description, 
                'price': place.price, 
                'latitude': place.latitude, 
                'longitude': place.longitude,
                'owner_id': place.owner_id
            }, 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        """Retrieve all places (Public access)"""
        places = facade.get_all_places()
        if not places:
            return {'error': 'No places found'}, 404
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude} for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public access)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {'id': place.owner.id, 'first_name': place.owner.first_name, 'last_name': place.owner.last_name, 'email': place.owner.email} if place.owner else None,
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities]
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def put(self, place_id):
        """Update a place (Authentication required - Owner only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if the authenticated user is the owner
        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload.copy()
        
        # Handle amenities if provided
        if 'amenities' in data:
            amenities = [facade.get_amenity(aid) for aid in data.get('amenities', []) if facade.get_amenity(aid)]
            data['amenities'] = amenities
        
        # Remove owner from data as it shouldn't be updated
        data.pop('owner', None)
        
        try:
            facade.update_place(place_id, data)
            return {'message': 'Place updated successfully'}, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400