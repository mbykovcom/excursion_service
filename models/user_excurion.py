from datetime import datetime

from pydantic import BaseModel, Field

from .excursion import ExcursionDetails


class UserExcursionIn(BaseModel):
    excursion: str = Field(..., description='Name excursion')
    last_point: int = Field(..., description='The point where we stopped')
    date_added: datetime = Field(..., description='Date added')


class UserExcursionOut(UserExcursionIn):
    id: int = Field(..., description='User excursion id')
    excursion: ExcursionDetails = Field(..., description='Data excursion')
    last_point: str = Field(..., description='Name of the point where we stopped')


class UserExcursion:
    def __init__(self, _id: int, id_user: int, id_excursion: int, last_point: int, date_added: datetime):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion: int = id_excursion
        self.last_point: int = last_point
        self.date_added: datetime = date_added
