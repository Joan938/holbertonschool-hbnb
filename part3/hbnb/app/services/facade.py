# hbnb/app/services/facade.py

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

    # … the rest of your methods (amenities, places, reviews) remain unchanged …
