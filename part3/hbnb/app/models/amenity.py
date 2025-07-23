import uuid
from app import db
from .place import place_amenity

class Amenity(db.Model):
    __tablename__ = 'amenities'
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)

    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities')