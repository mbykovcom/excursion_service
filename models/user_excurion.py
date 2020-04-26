from datetime import datetime

from pydantic import BaseModel, Field

from .excursion import ExcursionOut
from .excursion_point import ExcursionPointOut
from .user import UserOut


class UserExcursionOut(BaseModel):
    id: int = Field(..., description='User excursion id')
    id_user: int = Field(..., description='User id')
    id_excursion: int = Field(..., description='Excursion id')
    id_last_point: int = Field(..., description='The point where we stopped')
    is_active: bool = Field(..., description='Tour status, active 30 days after adding, then inactive')
    date_added: datetime = Field(..., description='Date added')


class UserExcursionDetail(BaseModel):
    id: int = Field(..., description='User excursion id')
    user: UserOut = Field(..., description='User data')
    excursion: ExcursionOut = Field(..., description='Data excursion')
    last_point: ExcursionPointOut = Field(..., description='Name of the point where we stopped')
    is_active: bool = Field(..., description='Tour status, active 30 days after adding, then inactive')
    date_added: datetime = Field(..., description='Date added')


class UserExcursion:
    def __init__(self, id_user: int, id_excursion: int, is_active: bool, date_added: datetime = datetime.now(),
                 id_last_point: int = 0, _id: int = None):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion: int = id_excursion
        self.id_last_point: int = id_last_point
        self.is_active: bool = is_active
        self.date_added: datetime = date_added

    def __repr__(self):
        return f"UserExcursion: {self._id} | user: {self.id_user} | excursion: {self.id_excursion} | " \
               f"last point: {self.id_last_point} | is_active: {self.is_active} | date added: {self.date_added}"

    def user_excursion_out(self):
        return UserExcursionOut(id=self._id, id_user=self.id_user, id_excursion=self.id_excursion,
                                id_last_point=self.id_last_point, is_active=self.is_active, date_added=self.date_added)
