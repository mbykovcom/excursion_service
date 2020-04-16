from typing import List

from pydantic import BaseModel, Field

from .object import ObjectOut, Object


class RouteIn(BaseModel):
    name: str = Field(..., description='The name of the route')
    route: List[int] = Field(..., description='Point sequential list of objects')


class RouteOut(RouteIn):
    id: int = Field(..., description='Route id')


class RouteDetails(RouteOut):
    route: List[ObjectOut] = Field(..., description='List of objects')


class Route:
    def __init__(self, _id: int, name: str, route: List[Object]):
        self._id: int = _id
        self.name: str = name
        self.route: List[Object] = route
