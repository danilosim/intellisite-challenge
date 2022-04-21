from beanie import Document


class VehicleDetection(Document):
    Year: int
    Make: str
    Model: str
    Category: str

    class Collection:
        name = "vehicles"


class User(Document):
    username: str
    password: str
    role: str

    class Collection:
        name = "users"
