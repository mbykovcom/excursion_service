from typing import List

from pydantic import BaseModel, Field

from models.excursion_point import ExcursionPoint


class ExcursionIn(BaseModel):
    name: str = Field(..., description='The name of the tour')
    description: str = Field(..., description='The description of the tour')
    price: float = Field(..., description='The cost of the tour')


class ExcursionOut(ExcursionIn):
    id: int = Field(..., description='Excursion id')
    url_map_route: str = Field(None, description='Url of the tour route on the map')


class ExcursionUpdate(BaseModel):
    name: str = Field(None, description='The name of the tour')
    description: str = Field(None, description='The description of the tour')
    price: float = Field(None, description='The cost of the tour')


class Excursion:
    def __init__(self, name: str, description: str, price: float, _id: int = None, url_map_route: str = None):
        self._id: int = _id
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.url_map_route: str = url_map_route

    def __repr__(self):
        return f"Excursion: {self._id} | {self.name} | {self.description} | {self.price} | {self.url_map_route}"

    def excursion_out(self):
        return ExcursionOut(id=self._id, name=self.name, description=self.description, price=self.price,
                            url_map_route=self.url_map_route)

    def create_url_map_route(self, list_point: List[ExcursionPoint]):
        pass
