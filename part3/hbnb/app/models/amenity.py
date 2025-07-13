from app.models.base import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name:
            raise ValueError("name cannot be empty")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if len(name) > 50:
            raise ValueError("name length must not exceed 50 characters")
        self.name = name