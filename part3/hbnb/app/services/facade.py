from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()


    """User methods"""
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(new_data)
        return user


    """Amenity methods"""
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
        return amenity
    

    """Place methods"""
    def create_place(self, place_data):
        if 'owner' in place_data:
            owner = place_data.pop('owner')
            owner_id = owner.get('id')
        else:
            owner_id = place_data.get('owner_id')
        place_data['owner_id'] = owner_id
        amenities = []
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                amenities.append(amenity)
            else:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
    
        # Ensure the Place object only has owner_id, not the full owner object
        place_data["amenities"] = amenities
        place = Place(**place_data)
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place:
            place.update(place_data)
        return place


    """Reviews methods"""
    def create_review(self, review_data):
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')
        if not user_id or not place_id:
            raise ValueError("User ID and Place ID must be provided.")
        review = Review(**review_data)
        place = self.get_place(place_id)
        if place:
            place.add_review(review)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if place:
            return place.reviews
        return []


    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.update(review_id, review_data)
        return review_data


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
        return {"message": "Review deleted successfully"}