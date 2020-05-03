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

    def __repr__(self):
        return f"Object: {self._id} | name: {self.name} | description: {self.description} | " \
               f"location: lat={self.location[0]} lon={self.location[1]}"

    def object_out(self):
        return ObjectOut(id=self._id, name=self.name, description=self.description, location={'lon': self.location[1],
                         'lat': self.location[0]})
