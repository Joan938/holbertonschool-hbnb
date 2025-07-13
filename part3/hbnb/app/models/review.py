from app.models.base import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        if not text:
            raise ValueError("text cannot be empty")
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self.text = text

        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if 1 > rating > 5:
            raise ValueError("rating must be between 1 - 5")
        self.rating = rating
        self.place_id = place_id
        self.place = self.get_place(self.place_id)
        self.user_id = user_id
        self.user = self.get_User(self.user_id)


    def get_place(self, id):
        from app.services import facade
        place = facade.get_place(id)
        return place
    

    def get_User(self, id):
        from app.services import facade
        user = facade.get_user(id)
        return user