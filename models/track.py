from pydantic import BaseModel, Field


class TrackIn(BaseModel):
    name: str = Field(..., description='The name of the track')


class TrackOut(TrackIn):
    id: int = Field(..., description='Track id')
    url: str = Field(..., description='Url of the file in S3 storage')


class TrackDetails(TrackOut):
    track: bytes = Field(..., description='Track data in binary form')


class TrackUpdate(BaseModel):
    name: str = Field(None, description='The name of the track')
    track: bytes = Field(None, description='Track data in binary form')


class Track:
    def __init__(self, name: str, url: str = None, _id: int = None):
        self._id: int = _id
        self.name: str = name
        self.url: str = url

    def __repr__(self):
        return f"Track: {self._id} | name: {self.name} | track in binary form: {self.url}"

    def track_out(self) -> TrackOut:
        return TrackOut(id=self._id, name=self.name, url=self.url)

    def track_details(self) -> TrackOut:
        return TrackDetails(id=self._id, name=self.name, track=self.url)
