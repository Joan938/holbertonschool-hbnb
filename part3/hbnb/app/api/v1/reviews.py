from flask_restx import Namespace, Resource, fields  # type: ignore
from app.services import facade

api = Namespace('reviews', description='Review operations')
review_model = api.model('Review', {
    'text':     fields.String(required=True),
    'rating':   fields.Integer(required=True),
    'user_id':  fields.String(required=True),
    'place_id': fields.String(required=True),
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        review = facade.create_review(api.payload)
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id}, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        reviews = facade.review_repo.get_all()
        if not reviews:
            return {'error': 'No reviews found'}, 404
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {'id': review.id, 'text': review.text, 'rating': review.rating, 'user_id': review.user_id, 'place_id': review.place_id}, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        data = api.payload
        updates = {}
        if 'text' in data:
            updates['text'] = data['text']
        if 'rating' in data:
            if not (isinstance(data['rating'], int) and 1 <= data['rating'] <= 5):
                return {'error': 'Rating must be an integer between 1 and 5'}, 400
            updates['rating'] = data['rating']
        facade.update_review(review_id, updates)
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewsList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if not reviews:
            return {'error': 'No reviews found for this place'}, 404
        return [{'id': r.id, 'text': r.text, 'rating': r.rating} for r in reviews], 200
