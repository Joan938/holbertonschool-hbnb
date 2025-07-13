from flask_restx import Namespace, Resource, fields  # type: ignore
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
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        data = api.payload
        place = facade.create_place(data)
        return {'id': place.id, 'title': place.title, 'description': place.description, 'price': place.price, 'latitude': place.latitude, 'longitude': place.longitude}, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        places = facade.place_repo.get_all()
        if not places:
            return {'error': 'No places found'}, 404
        return [{'id': p.id, 'title': p.title, 'latitude': p.latitude, 'longitude': p.longitude} for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
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
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        # update amenities list
        amenities = [facade.get_amenity(aid) for aid in data.get('amenities', []) if facade.get_amenity(aid)]
        data['amenities'] = amenities
        # update owner if provided
        if 'owner' in data:
            owner = facade.get_user(data['owner']['id'])
            data['owner_id'] = owner.id if owner else None
        facade.update_place(place_id, data)
        return {'message': 'Place updated successfully'}, 200

