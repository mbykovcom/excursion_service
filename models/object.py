from collections import namedtuple

from pydantic import BaseModel, Field

Coordinates = namedtuple('Coordinates', ['lat', 'lon'])


class ObjectIn(BaseModel):
    name: str = Field(..., description='The name of the object')
    description: str = Field(..., description='The description of a object')
    location: Coordinates = Field(..., description='The coordinates of the location')


class ObjectOut(ObjectIn):
    id: int = Field(..., description='Object id')


class Object:
    def __init__(self, _id: int, name: str, description: str, location: Coordinates):
        self._id: int = _id
        self.name: str = name
        self.description: str = description
        self.location: Coordinates = location
