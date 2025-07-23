from flask_restx import Namespace, Resource, fields  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')
review_model = api.model('Review', {
    'text':     fields.String(required=True),
    'rating':   fields.Integer(required=True),
    'place_id': fields.String(required=True),
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new review (Authentication required)"""
        current_user = get_jwt_identity()
        data = api.payload.copy()
        
        # Get the place to validate ownership and existence
        place = facade.get_place(data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400
        
        # Check if user is trying to review their own place
        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place'}, 400
        
        # Check if user has already reviewed this place
        if facade.user_has_reviewed_place(current_user, data['place_id']):
            return {'error': 'You have already reviewed this place'}, 400
        
        # Set the user_id to the authenticated user
        data['user_id'] = current_user
        
        try:
            review = facade.create_review(data)
            return {
                'id': review.id, 
                'text': review.text, 
                'rating': review.rating, 
                'user_id': review.user_id, 
                'place_id': review.place_id
            }, 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'No reviews found')
    def get(self):
        """Retrieve all reviews (Public access)"""
        reviews = facade.get_all_reviews()
        if not reviews:
            return {'error': 'No reviews found'}, 404
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public access)"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id, 
            'text': review.text, 
            'rating': review.rating, 
            'user_id': review.user_id, 
            'place_id': review.place_id
        }, 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (Authentication required - Author only)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if the authenticated user is the author of the review
        if review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        updates = {}
        
        if 'text' in data:
            updates['text'] = data['text']
        if 'rating' in data:
            if not (isinstance(data['rating'], int) and 1 <= data['rating'] <= 5):
                return {'error': 'Rating must be an integer between 1 and 5'}, 400
            updates['rating'] = data['rating']
        
        # Don't allow changing place_id or user_id
        updates.pop('place_id', None)
        updates.pop('user_id', None)
        
        try:
            facade.update_review(review_id, updates)
            return {'message': 'Review updated successfully'}, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(401, 'Authentication required')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (Authentication required - Author only)"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if the authenticated user is the author of the review
        if review.user_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewsList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (Public access)"""
        # First check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
            
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200