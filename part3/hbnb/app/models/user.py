# hbnb/app/models/user.py

import re
import uuid
from app import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36),
                   primary_key=True,
                   default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(50), unique=True, nullable=False)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        # Validation
        if not first_name or not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("Invalid first_name")
        if not last_name or not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("Invalid last_name")
        if not email or not isinstance(email, str) or len(email) > 50:
            raise ValueError("Invalid email")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        # Hash & store the password
        self.hash_password(password)

        # Assign the other fields
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.is_admin   = is_admin

    def hash_password(self, plaintext_password: str) -> None:
        """Hash a plaintext password and store its bcrypt hash."""
        self.password = bcrypt.generate_password_hash(
            plaintext_password
        ).decode('utf-8')

    def verify_password(self, plaintext_password: str) -> bool:
        """Check a plaintext password against the stored hash."""
        return bcrypt.check_password_hash(self.password, plaintext_password)
