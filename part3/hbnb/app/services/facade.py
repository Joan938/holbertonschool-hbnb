from app import db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        pass

    # ─── Users ──────────────────────────────────────────────────────────────────
    def create_user(self, user_data):
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        db.session.add(user)
        db.session.commit()
        return user

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_user_by_email(self, email):
        return User.query.filter_by(email=email).first()

    def get_all_users(self):
        return User.query.all()

    def update_user(self, user_id, new_data):
        user = User.query.get(user_id)
        if not user:
            return None
        for key, value in new_data.items():
            setattr(user, key, value)
        db.session.commit()
        return user

    # ─── Amenities ──────────────────────────────────────────────────────────────
    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get_amenity(self, amenity_id):
        return Amenity.query.get(amenity_id)

    def get_all_amenities(self):
        return Amenity.query.all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = Amenity.query.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        db.session.commit()
        return amenity

    # ─── Places ─────────────────────────────────────────────────────────────────
    def create_place(self, place_data):
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )
        
        # Handle amenities if provided
        if 'amenities' in place_data:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
        
        db.session.add(place)
        db.session.commit()
        return place

    def get_place(self, place_id):
        return Place.query.get(place_id)

    def get_all_places(self):
        return Place.query.all()

    def update_place(self, place_id, place_data):
        place = Place.query.get(place_id)
        if not place:
            return None
        
        # Update basic fields
        for key, value in place_data.items():
            if key not in ['amenities', 'owner']:
                setattr(place, key, value)
        
        # Handle amenities update
        if 'amenities' in place_data:
            place.amenities.clear()
            for amenity in place_data['amenities']:
                if hasattr(amenity, 'id'):  # If it's an amenity object
                    place.amenities.append(amenity)
                else:  # If it's an amenity ID
                    amenity_obj = self.get_amenity(amenity)
                    if amenity_obj:
                        place.amenities.append(amenity_obj)
        
        db.session.commit()
        return place

    # ─── Reviews ────────────────────────────────────────────────────────────────
    def create_review(self, review_data):
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )
        db.session.add(review)
        db.session.commit()
        return review

    def get_review(self, review_id):
        return Review.query.get(review_id)

    def get_all_reviews(self):
        return Review.query.all()

    def get_reviews_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def get_reviews_by_user(self, user_id):
        return Review.query.filter_by(user_id=user_id).all()

    def update_review(self, review_id, review_data):
        review = Review.query.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        review = Review.query.get(review_id)
        if not review:
            return False
        db.session.delete(review)
        db.session.commit()
        return True

    # ─── Helper Methods ─────────────────────────────────────────────────────────
    def user_has_reviewed_place(self, user_id, place_id):
        """Check if a user has already reviewed a specific place"""
        existing_review = Review.query.filter_by(
            user_id=user_id, 
            place_id=place_id
        ).first()
        return existing_review is not None

    # Create repository-like properties for backward compatibility
    @property
    def amenity_repo(self):
        class AmenityRepo:
            def get_all(self):
                return Amenity.query.all()
        return AmenityRepo()

    @property
    def place_repo(self):
        class PlaceRepo:
            def get_all(self):
                return Place.query.all()
        return PlaceRepo()

    @property
    def review_repo(self):
        class ReviewRepo:
            def get_all(self):
                return Review.query.all()
        return ReviewRepo()

# Create a single facade instance
facade = HBnBFacade()

