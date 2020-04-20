from pydantic import BaseModel, Field


class ExcursionIn(BaseModel):
    name: str = Field(..., description='The name of the tour')
    description: str = Field(..., description='The description of the tour')
    price: float = Field(..., description='The cost of the tour')


class ExcursionOut(ExcursionIn):
    id: int = Field(..., description='Excursion id')
    url_map_route: str = Field(..., description='Url of the tour route on the map')


class Excursion:
    def __init__(self, _id: int, name: str, description: str, price: float, url_map_route: str):
        self._id: int = _id
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.url_map_route: str = url_map_route
