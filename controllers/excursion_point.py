"""
Module for working with excursion points
"""

from typing import List

from fastapi import HTTPException
from starlette import status

from database import db
from models.excursion_point import ExcursionPoint

TABLE = 'excursion_points'


def create_excursion_point(point_data: ExcursionPoint) -> ExcursionPoint:
    """
    Add a new excursion point to the collection
    :param point_data: excursion point data
    :return: excursion point added to the collection
    """
    points = get_excursion_points_by_excursion(point_data.id_excursion)
    list_sequence = [point.sequence_number for point in points]
    if point_data.sequence_number in set(list_sequence):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='An excursion point with this ordinal '
                                                                            'number already exists')
    if list_sequence == [] and point_data.sequence_number > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This excursion point cannot be '
                                                                            f'{point_data.sequence_number} in the '
                                                                            'sequence, because there are no points '
                                                                            'in the route yet')
    if list_sequence != [] and point_data.sequence_number - list_sequence[-1] > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='This excursion point cannot be '
                                                                            f'{point_data.sequence_number} in the '
                                                                            'sequence, because the number of the last '
                                                                            f'point is {list_sequence[-1]}')
    if point_data._id is None:
        point_data._id = db.get_last_id(TABLE).last_id
    return db.add(point_data)


def delete_excursion_point(point_id: int) -> ExcursionPoint:
    """
    Delete an excursion point from the collection
    :param point_id: id of the excursion point to delete
    :return: excursion point deleted from the collection
    """
    deleted_point = db.get_data_by_id(point_id, TABLE)
    result = db.delete(point_id, TABLE)
    if result:
        return deleted_point
    else:
        return None


def get_excursion_point_by_id(point_id: int) -> ExcursionPoint:
    """
    Get an excursion point from the collection by id
    :param point_id: id of the excursion point you are looking for
    :return: desired excursion point
    """
    return db.get_data_by_id(point_id, TABLE)


def get_excursion_points() -> List[ExcursionPoint]:
    """
    Get all excursion points from the collection.
    :return: list of excursion points
    """
    return db.get_all_items(TABLE)


def get_excursion_points_by_excursion(excursion_id: int) -> List[ExcursionPoint]:
    """
    Get an excursion point from the collection by id excursion
    :param excursion_id: id of the excursion you are looking for
    :return: desired list of excursion points
    """
    return db.get_points(excursion_id)


def update_excursion_point(point_id: int, id_object: int = None, id_track: int = None) -> ExcursionPoint:
    """
    Updates an excursion point in the collection
    :param point_id: Excursion point id to update
    :param id_track: new id_track the excursion point
    :param id_object: new id_object the excursion point
    :return: updated excursion point
    """
    point = get_excursion_point_by_id(point_id)
    if not point:
        return None
    flag_update = False
    if id_object is not None:
        point.id_object = id_object
        flag_update = True
    if id_track is not None:
        point.id_track = id_track
        flag_update = True
    if not flag_update:
        return point
    if db.update_item(point):
        return point
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the excursion '
                                                                                      'point')


def check_track_in_excursion(excursion_id: int, track_id: int) -> ExcursionPoint:
    """
    Checking whether this track exists in the specified excursion
    :param excursion_id: id of the excursion
    :param track_id:  id of the track
    :return: If exists returns the excursion point, if not returns None
    """
    point = db.check_track_in_excursion(excursion_id, track_id)
    if point:
        return point
    else:
        return None