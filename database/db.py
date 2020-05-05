from datetime import datetime, timedelta
from typing import List, Union

from database.connection import Database
from models.excursion import Excursion
from models.excursion_point import ExcursionPoint
from models.listening import Listening
from models.object import Object
from models.other import TableKey
from models.track import Track
from models.user import User

# BASE
from models.user_excurion import UserExcursion


def add(data: Union[User, Object, Excursion, UserExcursion, Track, ExcursionPoint,
                    Listening]) -> Union[User, Object, Excursion, UserExcursion, Track, ExcursionPoint, Listening]:
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
    elif type(data) is Excursion:
        table = 'excursions'
    elif type(data) is UserExcursion:
        table = 'user_excursions'
    elif type(data) is Track:
        table = 'tracks'
    elif type(data) is ExcursionPoint:
        table = 'excursion_points'
    elif type(data) is Listening:
        table = 'listening'
    else:
        return False
    collection = db.get_collection(table)
    keys = db.get_collection('table_keys')
    try:
        last_raw = get_last_id(table)
        data._id = last_raw.last_id
        id = collection.insert_one(data.__dict__).inserted_id
        count = keys.update_one({'table': table}, {'$inc': {'last_id': 1}}).modified_count
        if type(id) is int and count == 1:
            return data
        else:
            collection.delete_one({'_id': id})
            if last_raw.last_id != 1:
                keys.update_one({'table': table}, {'$inc': {'last_id': -1}})
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


def delete_items_by_list_id(list_id: List[int], collection_name: str) -> bool:
    db = Database()
    collection = db.get_collection(collection_name)
    count = collection.delete_many({'_id': {'$in': list_id}}).deleted_count
    if count == len(list_id):
        return True
    else:
        return False


def update_item(update: Union[User, Object, Excursion, Track, ExcursionPoint, UserExcursion]) -> bool:
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
    elif type(update) is Excursion:
        table = 'excursions'
    elif type(update) is UserExcursion:
        table = 'user_excursions'
    elif type(update) is Track:
        table = 'tracks'
    elif type(update) is ExcursionPoint:
        table = 'excursion_points'
    else:
        return False
    try:
        collection = db.get_collection(table)
        modified = collection.update_one({'_id': update._id}, {'$set': update.__dict__}).modified_count
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        return None
    if modified:
        return True
    else:
        return False


def get_data_by_id(id: int, collection_name: str) -> Union[User, Object, Excursion, Track, ExcursionPoint,
                                                           UserExcursion]:
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
        elif collection_name == 'excursions':
            data = Excursion(**data)
        elif collection_name == 'tracks':
            data = Track(**data)
        elif collection_name == 'excursion_points':
            data = ExcursionPoint(**data)
        elif collection_name == 'user_excursions':
            data = UserExcursion(**data)
        else:
            return None
    return data


def get_all_items(collection_name: str) -> Union[List[User], List[Object], List[Excursion], List[UserExcursion],
                                                 List[Track], List[ExcursionPoint]]:
    """
    Get all objects from the collection
    :param collection_name: collection name
    :return: list of items
    """
    db = Database()
    collection = db.get_collection(collection_name)
    data = collection.find()
    if collection_name == 'users':
        list_items = [User(**user_data) for user_data in data]
    elif collection_name == 'objects':
        list_items = [Object(**obj_data) for obj_data in data]
    elif collection_name == 'excursions':
        list_items = [Excursion(**excursion_data) for excursion_data in data]
    elif collection_name == 'tracks':
        list_items = [Track(**track_data) for track_data in data]
    elif collection_name == 'excursion_points':
        list_items = [ExcursionPoint(**point_data) for point_data in data]
    elif collection_name == 'user_excursions':
        list_items = [UserExcursion(**user_excursion_data) for user_excursion_data in data]
    else:
        return None
    return list_items


def get_items_by_list_id(collection_name: str, list_id: List[int]) -> Union[List[User], List[Object], List[Excursion],
                                                                            List[UserExcursion], List[Track],
                                                                            List[ExcursionPoint]]:
    db = Database()
    collection = db.get_collection(collection_name)
    data = collection.find({'_id': {'$in': list_id}})
    if collection_name == 'users':
        list_items = [User(**user_data) for user_data in data]
    elif collection_name == 'objects':
        list_items = [Object(**obj_data) for obj_data in data]
    elif collection_name == 'excursions':
        list_items = [Excursion(**excursion_data) for excursion_data in data]
    elif collection_name == 'tracks':
        list_items = [Track(**track_data) for track_data in data]
    elif collection_name == 'excursion_points':
        list_items = [ExcursionPoint(**point_data) for point_data in data]
    elif collection_name == 'user_excursions':
        list_items = [UserExcursion(**user_excursion_data) for user_excursion_data in data]
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


# EXCURSIONS

def get_excursions() -> List[Excursion]:
    db = Database()
    collection = db.get_collection('excursions')
    data = collection.find({'url_map_route': {'$ne': None}})
    list_excursions = [Excursion(**excursion_data) for excursion_data in data]
    return list_excursions


def update_url(excursion: Excursion) -> bool:
    """
    Updates an url the excursion in the collection
    :param excursion: Excursion to update
    :return: result of updating
    """
    db = Database()
    try:
        collection = db.get_collection('excursions')
        modified = collection.update_one({'_id': excursion._id},
                                         {'$set': {'url_map_route': excursion.url_map_route}}).modified_count
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        return None
    if modified:
        return True
    else:
        return False


# EXCURSION POINTS

def get_points(excursion_id: int) -> List[ExcursionPoint]:
    db = Database()
    collection = db.get_collection('excursion_points')
    data = collection.find({'id_excursion': excursion_id}).sort('sequence_number')
    list_points = [ExcursionPoint(**point_data) for point_data in data]
    return list_points


def check_track_in_excursion(excursion_id: int, track_id: int) -> ExcursionPoint:
    db = Database()
    collection = db.get_collection('excursion_points')
    point_data = collection.find_one({'$and': [{'id_excursion': excursion_id}, {'id_track': track_id}]})
    if point_data:
        return ExcursionPoint(**point_data)
    else:
        return None


# TRACK

def get_track_by_name(name: str) -> Track:
    """
    Get a track by name
    :param name: track name
    :return: the desired track
    """
    db = Database()
    collection = db.get_collection('tracks')
    track_data = collection.find_one({'name': name})
    if track_data:
        return Track(**track_data)
    else:
        return None


# USER EXCURSIONS

def get_user_excursion_by_user_id(user_id: int) -> List[UserExcursion]:
    db = Database()
    collection = db.get_collection('user_excursions')
    data = collection.find({'$and': [
        {'id_user': user_id},
        {'is_active': True}]})
    list_user_excursions = [UserExcursion(**user_excursion_data) for user_excursion_data in data]
    return list_user_excursions


def deactivating_user_excursion(user_excursion_id: int) -> bool:
    db = Database()
    user_excursions = db.get_collection('user_excursions')
    try:
        count = user_excursions.update_one({'_id': user_excursion_id}, {'$set': {'is_active': False}}).modified_count
        if count == 1:
            return True
        else:
            return False
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        user_excursions.update_one({'_id': user_excursion_id}, {'$set': {'is_active': True}})
        return False


def check_user_excursion_is_active(excursion_id: int) -> UserExcursion:
    db = Database()
    collection = db.get_collection('user_excursions')
    data = collection.find_one({'$and': [
        {'id_excursion': excursion_id},
        {'is_active': True}]})
    if data:
        return UserExcursion(**data)
    else:
        return None


def get_expired_user_excursions(days: int) -> List[UserExcursion]:
    db = Database()
    collection = db.get_collection('user_excursions')
    date = datetime.now() - timedelta(days=days)
    user_excursions = collection.find({'$and': [
        {'is_active': True},
        {'date_added': {'$lt': date}}]})
    if user_excursions:
        return [UserExcursion(**user_excursion) for user_excursion in user_excursions]
    else:
        return None


# STATISTICS

def get_user_statistics(start: datetime, end: datetime) -> int:
    db = Database()
    collection = db.get_collection('users')
    users = collection.find({'$and': [
        {'is_active': True},
        {'date_registration': {'$gt': start}},
        {'date_registration': {'$lt': end}}]})
    return users.count()


def get_excursion_statistics(start: datetime, end: datetime) -> int:
    db = Database()
    collection = db.get_collection('user_excursions')
    user_excursions = collection.find({'$and': [
        {'date_added': {'$gt': start}},
        {'date_added': {'$lt': end}}]})
    return user_excursions.count()


def get_listening_statistics(start: datetime, end: datetime) -> int:
    db = Database()
    collection = db.get_collection('listening')
    user_excursions = collection.find({'$and': [
        {'date_listening': {'$gt': start}},
        {'date_listening': {'$lt': end}}]})
    return user_excursions.count()


def get_sales_statistics(start: datetime, end: datetime):
    db = Database()
    collection = db.get_collection('user_excursions')
    groups = collection.aggregate([
        {'$match': {'$and': [
            {'date_added': {'$gt': start}},
            {'date_added': {'$lt': end}}]}},
        {"$group": {"_id": "$id_excursion", "count": {"$sum": 1}}}
    ])
    return [group for group in groups]


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
