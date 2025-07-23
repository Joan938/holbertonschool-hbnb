from app import db

class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'), nullable=False)

    state = db.relationship('State', back_populates='cities')
    places = db.relationship('Place', back_populates='city', cascade='all, delete')