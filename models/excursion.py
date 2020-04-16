from pydantic import BaseModel, Field

from .route import RouteDetails


class ExcursionIn(BaseModel):
    id_route: int = Field(..., description='Route id')
    name: str = Field(..., description='The name of the tour')
    description: str = Field(..., description='The description of the tour')
    price: float = Field(..., description='The cost of the tour')


class ExcursionOut(ExcursionIn):
    id: int = Field(..., description='Excursion id')


class ExcursionDetails(BaseModel):
    id: int = Field(..., description='Excursion id')
    name: str = Field(..., description='The name of the tour')
    description: str = Field(..., description='The description of the tour')
    price: float = Field(..., description='The cost of the tour')
    route: RouteDetails = Field(..., description='RouteDetails object')


class Excursion:
    def __init__(self, _id: int, id_route: int, name: str, description: str, price: float):
        self._id: int = _id
        self.id_route: int = id_route
        self.name: str = name
        self.description: str = description
        self.price: float = price
