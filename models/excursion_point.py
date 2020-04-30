from typing import List

from pydantic import BaseModel, Field

from .object import ObjectOut, Object
from .track import TrackOut

from controllers import object as object_service


class ExcursionPointIn(BaseModel):
    id_excursion: int = Field(..., description='Excursion id')
    id_object: int = Field(..., description='Object id')
    id_track: int = Field(..., description='Track id')
    sequence_number: int = Field(..., description='Sequence of point in the route')


class ExcursionPointOut(ExcursionPointIn):
    id: int = Field(..., description='Excursion point id')


class ExcursionPointUpdate(BaseModel):
    id_object: int = Field(None, description='Object id')
    id_track: int = Field(None, description='Track id')


class ExcursionPointDetails(BaseModel):
    id: int = Field(..., description='Excursion point id')
    excursion: ExcursionPointOut = Field(..., description='Excursion data')
    object: ObjectOut = Field(..., description='Object data')
    track: TrackOut = Field(..., description='Track data')
    sequence_number: int = Field(..., description='Sequence of point in the route')


class ExcursionPoint:
    def __init__(self, id_excursion: int, id_object: int, id_track: int, sequence_number: int, _id: int = None):
        self._id: int = _id
        self.id_excursion: int = id_excursion
        self.id_object: int = id_object
        self.id_track: int = id_track
        self.sequence_number: int = sequence_number

    def __repr__(self):
        return f"Excursion Point: {self._id} | excursion id: {self.id_excursion} | object id: {self.id_object} | " \
               f"track id: {self.id_track} | sequence number: {self.sequence_number}"

    def excursion_point_out(self):
        return ExcursionPointOut(id=self._id, id_excursion=self.id_excursion, id_object=self.id_object,
                                 id_track=self.id_track, sequence_number=self.sequence_number)

    def get_object(self) -> Object:
        return object_service.get_object_by_id(self.id_object)
