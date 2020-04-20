from typing import List

from pydantic import BaseModel, Field

from .object import ObjectOut, Object
from .track import TrackOut


class ExcursionPointIn(BaseModel):
    id_excursion: int = Field(..., description='Excursion id')
    id_object: int = Field(..., description='Object id')
    id_track: int = Field(..., description='Track id')
    sequence_number: int = Field(..., description='Sequence of point in the route')


class ExcursionPointOut(ExcursionPointIn):
    id: int = Field(..., description='Excursion point id')


class ExcursionPointDetails(BaseModel):
    id: int = Field(..., description='Excursion point id')
    excursion: ExcursionPointOut = Field(..., description='Excursion data')
    object: ObjectOut = Field(..., description='Object data')
    track: TrackOut = Field(..., description='Track data')
    sequence_number: int = Field(..., description='Sequence of point in the route')


class ExcursionPoint:
    def __init__(self, _id: int, id_excursion: int, id_object: int, id_track: int, sequence_number: int):
        self._id: int = _id
        self.id_excursion: int = id_excursion
        self.id_object: int = id_object
        self.id_track: int = id_track
        self.sequence_number: int = sequence_number
