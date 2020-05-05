"""
Module for working with user excursions
"""

from typing import List

from fastapi import HTTPException
from starlette import status

from database import db
from models.excursion_point import ExcursionPointDetails
from models.user_excurion import UserExcursion, UserExcursionsDetail, UserExcursionDetail

from controllers import excursion as excursion_service
from controllers import excursion_point as point_service
from controllers import object as object_service
from controllers import track as track_service

TABLE = 'user_excursions'


def create_user_excursion(user_id: int, excursion_id: int) -> UserExcursion:
    """
    Add a new user excursion to the collection
    :param user_id: user id
    :param excursion_id: excursion id
    :return: user excursion added to the collection
    """
    new_user_excursion = UserExcursion(user_id, excursion_id, True)
    new_user_excursion._id = db.get_last_id(TABLE).last_id
    return db.add(new_user_excursion)


def deactivate_user_excursion(user_excursion_id: int) -> UserExcursion:
    """
    Deactivating a user's tour after 30 days of purchase
    :param user_excursion_id: id of the user excursion to deactivating
    :return: user excursion deactivated
    """
    user_excursion = db.get_data_by_id(user_excursion_id, TABLE)
    if user_excursion:
        if db.deactivating_user_excursion(user_excursion_id):
            user_excursion.is_active = False
            return user_excursion
        else:
            return None
    return None


def get_user_excursions_by_user_id(user_id: int) -> List[UserExcursion]:
    """
    Get all active user excursion of this user
    :param user_id: id of the user you are looking for
    :return: list of user excursion
    """
    return db.get_user_excursion_by_user_id(user_id)


def get_user_excursion_by_id(id: int) -> UserExcursion:
    """
    Get an object from the collection by id
    :param id: id of the object you are looking for
    :return: desired object
    """
    return db.get_data_by_id(id, TABLE)


def update_last_point(user_excursion: UserExcursion) -> UserExcursion:
    """
    Updates an excursion in the collection
    :param user_excursion: update the data user excursion
    :return: updated user excursion
    """
    if db.update_item(user_excursion):
        return user_excursion
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the last point')


def user_excursions_detail(user_excursion: UserExcursion) -> UserExcursionDetail:
    """
    Generate detailed information about an user excursion with detailed information about the last excursion point
    :param user_excursion: object UserExcursion
    :return: detailed information about an user excursion
    """
    excursion = excursion_service.get_excursion_by_id(user_excursion.id_excursion).excursion_out()
    if user_excursion.id_last_point == 0:
        point = point_service.get_excursion_points_by_excursion(user_excursion.id_excursion)[0]
    else:
        point = point_service.get_excursion_point_by_id(user_excursion.id_last_point)
    obj = object_service.get_object_by_id(point.id_object).object_out()
    track = track_service.get_track_by_id(point.id_track).track_out()
    last_excursion_point = ExcursionPointDetails(id=point._id, sequence_number=point.sequence_number, object=obj,
                                                 track=track)
    return UserExcursionDetail(id=user_excursion._id, excursion=excursion, last_point=last_excursion_point,
                               is_active=user_excursion.is_active, date_added=user_excursion.date_added)


def user_excursion_detail(user_excursion: UserExcursion) -> UserExcursionsDetail:
    """
    Generate detailed information about an user excursion with a detailed list of all points on this user excursion
    :param user_excursion: object UserExcursion
    :return: detailed information about an user excursion
    """
    excursion = excursion_service.get_excursion_by_id(user_excursion.id_excursion).excursion_out()
    points = point_service.get_excursion_points_by_excursion(user_excursion.id_excursion)
    list_point = []
    list_object = object_service.get_objects_by_list_id([point.id_object for point in points])
    list_track = track_service.get_tracks_by_list_id([point.id_track for point in points])
    for obj, track, point in zip(list_object, list_track, points):
        list_point.append(ExcursionPointDetails(id=point._id, sequence_number=point.sequence_number,
                                                object=obj.object_out(), track=track.track_out()))
    return UserExcursionsDetail(id=user_excursion._id, excursion=excursion, list_point=list_point,
                                is_active=user_excursion.is_active, date_added=user_excursion.date_added)
