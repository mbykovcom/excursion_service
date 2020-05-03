from pydantic import BaseModel, Field

from config import Config
from controllers import excursion_point as point_service
from controllers import object as object_service


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

    def create_url_map_route(self):
        points = point_service.get_excursion_points_by_excursion(self._id)
        if not points:
            self.url_map_route = None
            return self.url_map_route
        avg_lat, avg_lon = 0.0, 0.0
        map_points = ''
        list_id = [point.id_object for point in points]
        list_objects = object_service.get_objects_by_list_id(list_id)
        for obj, point in zip(list_objects, points):
            lat = obj.location[0]
            lon = obj.location[1]
            map_points += f'{lon},{lat},pmwtm{point.sequence_number}~'
            avg_lat += float(lat)
            avg_lon += float(lon)
        avg_lon = avg_lon/len(points)
        avg_lat = avg_lat/len(points)
        self.url_map_route = f'{Config.MAP}ll={avg_lon},{avg_lat}&z={Config.ZOOM_MAP}&l={Config.TYPE_MAP}' \
                             f'&pt={map_points[:-1]}'   # -1 to remove the unnecessary one at the end ~
        return self.url_map_route
