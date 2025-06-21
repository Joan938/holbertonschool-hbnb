from app.models.base import BaseModel
import re


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name:
            raise ValueError("Invalid input data")
        if not isinstance(first_name, str):
            raise TypeError("Invalid input data")
        if len(first_name) > 50:
            raise ValueError("Invalid input data")
        self.first_name = first_name

        if not last_name:
            raise ValueError("Invalid input data")
        if not isinstance(last_name, str):
            raise TypeError("Invalid input data")
        if len(last_name) > 50:
            raise ValueError("Invalid input data")
        self.last_name = last_name

        if not email:
            raise ValueError("Invalid input data")
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        if not isinstance(email, str):
            raise TypeError("Invalid input data")
        if len(email) > 50:
            raise ValueError("Invalid input data")
        self.email = email
        self.is_admin = is_admin
        self.places = []


    def add_place(self, obj):
        self.places.append(obj)