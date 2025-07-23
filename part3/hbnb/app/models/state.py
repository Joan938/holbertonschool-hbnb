from app import db

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    cities = db.relationship('City', back_populates='state', cascade='all, delete')