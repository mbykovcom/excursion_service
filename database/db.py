from datetime import datetime, timedelta
from typing import List, Union

from database.connection import Database
from models.object import Object
from models.other import TableKey
from models.user import User


# BASE

def add(data: Union[User, Object]) -> Union[User, Object]:
    """
    Adds an object to the collection
    :param data: object to add to the collection
    :return: added object
    """
    db = Database()
    if type(data) is User:
        table = 'users'
    elif type(data) is Object:
        table = 'objects'
    else:
        return False
    collection = db.get_collection(table)
    keys = db.get_collection('table_keys')
    try:
        last_raw = get_last_id(table)
        data._id = last_raw.last_id
        id = collection.insert_one(data.__dict__).inserted_id
        count = keys.update_one({'table': table}, {'$inc': {'last_id': 1}}, upsert=True).modified_count
        if type(id) is int and count == 1:
            return data
        else:
            collection.delete_one({'_id': id})
            if last_raw.last_id != 1:
                keys.update_one({'table': table}, {'$inc': {'last_id': -1}}, upsert=True)
            return None
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        return None


def delete(id: int, collection_name: str) -> bool:
    """
    Deletes an object from the collection by id
    :param id: object id
    :param collection_name: name of the collection to delete from
    :return: result of operation
    """
    db = Database()
    collection = db.get_collection(collection_name)
    count = collection.delete_one({'_id': id}).deleted_count
    if count:
        return True
    else:
        return False


def update_item(update: Union[User, Object]) -> bool:
    """
    Updates an object in the collection
    :param update: Object to update
    :return: result of updating
    """
    db = Database()
    if type(update) is User:
        table = 'users'
    elif type(update) is Object:
        table = 'objects'
    else:
        return False
    collection = db.get_collection(table)
    modified = collection.update_one({'_id': update._id}, {'$set': update.__dict__}).modified_count
    if modified:
        return True
    else:
        return False


def get_data_by_id(id: int, collection_name: str) -> Union[User, Object]:
    """
    Get an item from the collection by id
    :param id: id of the item you are looking for
    :param collection_name: name of the collection to search in
    :return: desired item
    """
    db = Database()
    collection = db.get_collection(collection_name)
    data = collection.find_one({'_id': id})
    if data:
        if collection_name == 'users':
            data = User(**data)
        elif collection_name == 'objects':
            data = Object(**data)
        else:
            return None
    return data


def get_all_items(collection_name: str):
    """
    Get all objects from the collection
    :param collection_name: сollection name
    :return: list of items
    """
    db = Database()
    collection = db.get_collection(collection_name)
    data = collection.find()
    if collection_name == 'users':
        list_items = [User(**user_data) for user_data in data]
    elif collection_name == 'objects':
        list_items = [Object(**obj_data) for obj_data in data]
    else:
        return None
    return list_items


# USERS

def get_user_by_email(email: str) -> User:
    """
        Get a user by email
        :param email: user's email address
        :return: the desired user
        """
    db = Database()
    collection = db.get_collection('users')
    user_data = collection.find_one({'email': email})
    if user_data:
        return User(**user_data)
    else:
        return None


def activate_user(email: str):
    """
       Activates the user in the service
       :param email: user's email address
       :return: activation result
       """
    db = Database()
    users = db.get_collection('users')
    try:
        count = users.update_one({'email': email}, {'$set': {'is_active': True}}).modified_count
        if count == 1:
            return True
        else:
            return None
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        users.update_one({'email': email}, {'$set': {'is_active': False}})
        return False


def get_inactive(hour: int = None) -> List[User]:
    """
        Get a list of users who are inactive within N hours after registration
        :return: list of inactive users
        """
    db = Database()
    collection = db.get_collection('users')
    if hour is None:
        users = collection.find({'is_active': False})
    else:
        date = datetime.now() - timedelta(hours=24)
        users = collection.find({'$and': [
            {'is_active': False},
            {'date_registration': {'$lt': date}}]})
    if users:
        return [User(**user) for user in users]
    else:
        return None


def delete_users(list_id: List[int]):
    """
              Delete an users from the collection
              :param list_id: list of user IDs to delete
              :return: the result of the removal
              """
    db = Database()
    collection = db.get_collection('users')
    count = collection.delete_many({'_id': {'$in': list_id}}).deleted_count
    if count:
        return True
    else:
        return False


# TABLE KEYS

def add_key(table: str, last_id: int = 1) -> TableKey:
    """
    Create an entry in the table about the last collection id
    :param table: collection name
    :param last_id: last id in the collection
    :return: Data about the collection and its latest id
    """
    db = Database()
    collection = db.get_collection('table_keys')
    key_id = collection.insert_one({'table': table, 'last_id': last_id}).inserted_id
    return TableKey(_id=key_id, table=table, last_id=last_id)


def get_last_id(table: str) -> TableKey:
    """
    Get the latest id in the collection
    :param table: collection name
    :return: Data about the collection and its latest id
    """
    db = Database()
    collection = db.get_collection('table_keys')
    key = collection.find_one({'table': table})
    if key is None:
        return add_key(table)
    return TableKey(**key)
