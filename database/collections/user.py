from datetime import datetime, timedelta
from typing import List

from database.collections.table_key import get_last_id
from database.connection import Database
from models.user import User


def get_user_by_email(email: str) -> User:
    db = Database()
    collection = db.get_collection('users')
    user_data = collection.find_one({'email': email})
    if user_data:
        return User(**user_data)
    else:
        return None


def get_user_by_id(id: int) -> User:
    db = Database()
    collection = db.get_collection('users')
    user_data = collection.find_one({'_id': id})
    if user_data:
        return User(**user_data)
    else:
        return None


def add_user(user: User) -> bool:
    db = Database()
    users = db.get_collection('users')
    keys = db.get_collection('table_keys')
    try:
        last_raw = get_last_id('users')
        if last_raw.last_id == 0:
            last_raw.last_id += 1
        user._id = last_raw.last_id
        user_id = users.insert_one(user.__dict__).inserted_id
        count = keys.update_one({'table': 'users'}, {'$inc': {'last_id': 1}}, upsert=True).modified_count
        if type(user_id) is int and count == 1:
            return True
        else:
            users.delete_one({'_id': user_id})
            keys.update_one({'table': 'users'}, {'$inc': {'last_id': -1}}, upsert=True)
            return False
    except BaseException as e:  # If an exception is raised when adding to the database
        print(f'Error: {e}')
        return False


def activate(email: str):
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


def delete_user(id: int) -> bool:
    db = Database()
    collection = db.get_collection('users')
    count = collection.delete_one({'_id': id}).deleted_count
    if count:
        return True
    else:
        return False


def delete_users(list_id: List[int]):
    db = Database()
    collection = db.get_collection('users')
    count = collection.delete_many({'_id': {'$in': list_id}}).deleted_count
    if count:
        return True
    else:
        return False
