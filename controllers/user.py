from datetime import timedelta
from typing import List

from config import Config
from database import db
from models.other import Token
from models.user import UserAuth, User
from utils import auth


def create_user(user_data: User) -> User:
    """
       Add a new user to the collection
       :param user_data: user data
       :return: user added to the collection
       """
    if user_data._id is None:
        user_data._id = db.get_last_id('users').last_id
    return db.add(user_data)


def activate_user(email: str) -> bool:
    """
    Activates the user in the service
    :param email: user's email address
    :return: activation result
    """
    return db.activate_user(email)


def get_user_by_email(email: str) -> User:
    """
    Get a user by email
    :param email: user's email address
    :return: the desired user
    """
    return db.get_user_by_email(email)


def login(user_data: UserAuth) -> Token:
    """
    Logging in to the service and getting a token
    :param user_data: authorization data
    :return: Json Web Token
    """
    db_user = db.get_user_by_email(user_data.email)
    if db_user:
        if db_user.is_active is True:
            if auth.verify_password(user_data.password, db_user.hash_password):
                access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = auth.create_access_token(
                    data={"sub": user_data.email}, expires_delta=access_token_expires
                )
                return Token(access_token=access_token, token_type="bearer")
    return None


def get_users_inactive_24_hours() -> List[User]:
    """
    Get a list of users who are inactive within 24 hours after registration
    :return: list of inactive users
    """
    return db.get_inactive(24)


def delete_user(id: int) -> User:
    """
        Delete an user from the collection
        :param id: id of the user to delete
        :return: user deleted from the collection
        """
    user = db.get_data_by_id(id, 'users')
    if user:
        if db.delete(id, 'users'):
            return user
    return None


def delete_users(list_id: List[int]) -> bool:
    """
           Delete an users from the collection
           :param list_id: list of user IDs to delete
           :return: the result of the removal
           """
    return db.delete_users(list_id)
