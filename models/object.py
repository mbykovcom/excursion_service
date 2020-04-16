from collections import namedtuple

from pydantic import BaseModel, Field

Coordinates = namedtuple('Coordinates', ['lat', 'lon'])


class ObjectIn(BaseModel):
    name: str = Field(..., description='')
    location: Coordinates = Field(..., description='The coordinates of the location')
    url_audio: str = Field(..., description='Url audio')


class ObjectOut(ObjectIn):
    id: int = Field(..., description='Object id')


class Object:
    def __init__(self, _id: int, name: str, location: Coordinates, url_audio: str):
        self._id: int = _id
        self.name: str = name
        self.location: Coordinates = location
        self.url_audio: str = url_audio
