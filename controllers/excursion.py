from typing import List

from fastapi import HTTPException
from starlette import status

from database import db
from models.excursion import Excursion, ExcursionIn, ExcursionUpdate
from models.user_excurion import UserExcursion

from controllers import excursion_point as point_service
TABLE = 'excursions'


def create_excursion(excursion_data: Excursion) -> Excursion:
    """
    Add a new excursion to the collection
    :param excursion_data: excursion data
    :return: excursion added to the collection
    """
    if excursion_data._id is None:
        excursion_data._id = db.get_last_id(TABLE).last_id
    return db.add(excursion_data)


def delete_excursion(excursion_id: int) -> Excursion:
    deleted_excursion = db.get_data_by_id(excursion_id, TABLE)
    result = db.delete(excursion_id, TABLE)
    if result:
        points = point_service.get_excursion_points_by_excursion(excursion_id)
        list_point_id = [point._id for point in points]
        if db.delete_items_by_list_id(list_point_id, 'excursion_points'):
            return deleted_excursion
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='The excursion was deleted, '
                                                                                          'but was not already deleted '
                                                                                          'excursion points')
    else:
        return None


def get_excursion_by_id(excursion_id: int) -> Excursion:
    return db.get_data_by_id(excursion_id, TABLE)


def get_excursions(role: str) -> List[Excursion]:
    if role == 'user':
        return db.get_excursions()
    else:
        return db.get_all_items(TABLE)


def update_excursion(excursion_id: int, excursion_update: ExcursionUpdate) -> Excursion:
    """
       Updates an excursion in the collection
       :param excursion_id: Excursion id to update
       :param excursion_update: update the data excursion
       :return: updated excursion
       """
    excursion = get_excursion_by_id(excursion_id)
    if not excursion:
        return None
    flag_update = False
    if excursion_update.name is not None:
        excursion.name = excursion_update.name
        flag_update = True
    if excursion_update.description is not None:
        excursion.description = excursion_update.description
        flag_update = True
    if excursion_update.price is not None:
        excursion.price = excursion_update.price
        flag_update = True
    if not flag_update:
        return excursion
    if db.update_item(excursion):
        return excursion
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the excursion')


def buy_excursion(excursion_id: int, user_id: int) -> UserExcursion:
    excursion = get_excursion_by_id(excursion_id)
    if excursion and excursion.url_map_route is not None:
        user_excursion = UserExcursion(user_id, excursion_id, True)
        user_excursion._id = db.get_last_id(TABLE).last_id
        return db.add(user_excursion)
    else:
        return None


def update_url_map_route(excursion_id: int) -> Excursion:
    excursion = get_excursion_by_id(excursion_id)
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')
    if db.update_url(excursion):
        return excursion
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the excursion')