from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)