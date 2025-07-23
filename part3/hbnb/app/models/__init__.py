# import all models so that db.create_all() sees them
from .state import State
from .city import City
from .user import User
from .place import Place
from .amenity import Amenity
from .review import Review