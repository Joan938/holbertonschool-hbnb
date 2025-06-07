classDiagram
    class BaseModel {
        +UUID id
        +datetime created_at
        +datetime updated_at
        +save()
        +delete()
    }

    class User {
        +str first_name
        +str last_name
        +str email
        +str password
        +bool is_admin
        +update_profile()
    }

    class Place {
        +str title
        +str description
        +float price
        +float latitude
        +float longitude
        +create()
        +update()
        +delete()
        +list_amenities()
    }

    class Review {
        +int rating
        +str comment
        +create()
        +update()
        +delete()
    }

    class Amenity {
        +str name
        +str description
        +create()
        +update()
        +delete()
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "*" Place : owns
    User "1" --> "*" Review : writes
    Place "1" --> "*" Review : receives
    Place "1" --> "*" Amenity : includes
