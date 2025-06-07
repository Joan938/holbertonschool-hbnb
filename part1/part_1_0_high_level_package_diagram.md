classDiagram
    class PresentationLayer {
        <<Interface>>
        +APIService
        +UserController
        +PlaceController
        +ReviewController
        +AmenityController
    }

    class BusinessLogicLayer {
        +UserService
        +PlaceService
        +ReviewService
        +AmenityService
        +Models: User, Place, Review, Amenity
    }

    class PersistenceLayer {
        +UserRepository
        +PlaceRepository
        +ReviewRepository
        +AmenityRepository
        +Database (Storage)
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern\n(Request Handling)
    BusinessLogicLayer --> PersistenceLayer : Data Access (CRUD)

