from typing import List

from database import db
from models.object import Object


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


def edit_object(new_object_data: Object):
    pass
