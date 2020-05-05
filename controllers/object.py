"""
Module for working with object
"""

from typing import List

from fastapi import HTTPException
from starlette import status

from database import db
from models.object import Object, ObjectUpdate, Coordinates


def create_object(object_data: Object) -> Object:
    """
    Add a new object to the collection
    :param object_data: object data
    :return: object added to the collection
    """
    if object_data._id is None:
        object_data._id = db.get_last_id('objects').last_id
    return db.add(object_data)


def delete_object(id: int) -> Object:
    """
    Delete an object from the collection
    :param id: id of the object to delete
    :return: object deleted from the collection
    """
    obj = db.get_data_by_id(id, 'objects')
    if obj:
        if db.delete(id, 'objects'):
            return obj
    return None


def get_objects() -> List[Object]:
    """
    Get all objects from the collection
    :return: list of objects
    """
    return db.get_all_items('objects')


def get_object_by_id(id: int) -> Object:
    """
    Get an object from the collection by id
    :param id: id of the object you are looking for
    :return: desired object
    """
    return db.get_data_by_id(id, 'objects')


def update_object(object_id: int, obj_update: ObjectUpdate) -> Object:
    """
   Updates an object in the collection
   :param object_id: Object id to update
   :param obj_update: update the data object
   :return: updated object
   """
    obj = get_object_by_id(object_id)
    if not obj:
        return None
    if obj_update.name is not None:
        obj.name = obj_update.name
    if obj_update.description is not None:
        obj.description = obj_update.description
    if obj_update.location is not None:
        obj.location = Coordinates(lat=obj_update.location['lat'], lon=obj_update.location['lon'])
    if db.update_item(obj):
        return obj
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the object')


def get_objects_by_list_id(list_id: List[int]) -> List[Object]:
    """
    Get an list object from the collection by list id
    :param list_id: list id of the object you are looking for
    :return: desired list object
    """
    list = db.get_items_by_list_id('objects', list_id)
    return list
