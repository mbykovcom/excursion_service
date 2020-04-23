from collections import namedtuple

from pydantic import BaseModel, Field

Coordinates = namedtuple('Coordinates', ['lat', 'lon'])


class ObjectIn(BaseModel):
    name: str = Field(..., description='The name of the object')
    description: str = Field(..., description='The description of a object')
    location: dict = Field(..., description='The coordinates of the location')


class ObjectUpdate(BaseModel):
    name: str = Field(None, description='The name of the object')
    description: str = Field(None, description='The description of a object')
    location: dict = Field(None, description='The coordinates of the location')


class ObjectOut(ObjectIn):
    id: int = Field(..., description='Object id')


class Object:
    def __init__(self, name: str, description: str, location: Coordinates, _id: int = None):
        self._id: int = _id
        self.name: str = name
        self.description: str = description
        self.location: Coordinates = location

    def object_out(self):
        return ObjectOut(id=self._id, name=self.name, description=self.description, location=self.location)
