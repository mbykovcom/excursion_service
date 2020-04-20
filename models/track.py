from pydantic import BaseModel, Field


class TrackIn(BaseModel):
    name: str = Field(..., description='The name of the track')
    url: str = Field(..., description='Url of the track')


class TrackOut(TrackIn):
    id: int = Field(..., description='Track id')


class Track:
    def __init__(self, _id: int, name: str, url: str,):
        self._id: int = _id
        self.name: str = name
        self.url: str = url
