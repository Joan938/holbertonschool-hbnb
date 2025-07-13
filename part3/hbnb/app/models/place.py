from app.models.base import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities=[]):
        super().__init__()
        if not title:
            raise ValueError("title cannot be empty")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if len(title) > 100:
            raise ValueError("title length must not exceed 50 characters")
        self.title = title

        if not isinstance(description, str):
            raise TypeError("description must be a string")
        self.description = description

        if not isinstance(price, float):
            raise TypeError("price must be a float")
        if price < 0.0:
            raise ValueError("price must be a non negative float")
        self.price = price

        if not isinstance(latitude, float):
            raise TypeError("latitude must be a float")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude is out of range")
        self.latitude = latitude

        if not isinstance(longitude, float):
            raise TypeError("longitude must be a float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude is out of range")
        self.longitude = longitude
        self.owner_id = owner_id
        self.owner = self.get_owner(self.owner_id)
        self.amenities = amenities
        self.reviews = []


    def get_owner(self, id):
        from app.services import facade
        var = facade.get_user(id)
        return var


    def add_amenities(self, amenity):
        self.amenities.append(amenity)


    def add_review(self, review):
        self.reviews.append(review)