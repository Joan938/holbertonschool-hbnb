import uuid
from app import db

# Association table for many-to-many relationship between places and amenities
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(db.Model):
    __tablename__ = 'places'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = db.relationship('User', backref='places')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        if not title:
            raise ValueError("title cannot be empty")
        if not isinstance(title, str):
            raise TypeError("title must be a string")
        if len(title) > 100:
            raise ValueError("title length must not exceed 100 characters")
        
        if not isinstance(description, str):
            raise TypeError("description must be a string")
        
        if not isinstance(price, (int, float)):
            raise TypeError("price must be a number")
        if price < 0.0:
            raise ValueError("price must be a non negative number")
        
        if not isinstance(latitude, (int, float)):
            raise TypeError("latitude must be a number")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude is out of range")
        
        if not isinstance(longitude, (int, float)):
            raise TypeError("longitude must be a number")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude is out of range")

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)  
        self.longitude = float(longitude)
        self.owner_id = owner_id

# File path: part3/hbnb/app/models/review.py
import uuid
from app import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    user = db.relationship('User', backref='reviews')

    def __init__(self, text, rating, place_id, user_id):
        if not text:
            raise ValueError("text cannot be empty")
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")
        
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

# File path: part3/hbnb/app/models/amenity.py
import uuid
from app import db

class Amenity(db.Model):
    __tablename__ = 'amenities'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name):
        if not name:
            raise ValueError("name cannot be empty")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) > 50:
            raise ValueError("name length must not exceed 50 characters")
        
        self.name = name

