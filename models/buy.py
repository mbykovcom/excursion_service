from datetime import datetime

from pydantic import BaseModel, Field


class BuyIn(BaseModel):
    id_excursion: int = Field(..., description='Excursion id')
    id_user: int = Field(..., description='User id')


class Buy:
    def __init__(self, _id: int, id_user: int, id_excursion: int, date_buy: datetime):
        self._id: int = _id
        self.id_user: int = id_user
        self.id_excursion: int = id_excursion
        self.date_buy: datetime = date_buy