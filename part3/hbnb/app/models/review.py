import uuid
from app import db

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)

    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')