from datetime import timedelta
from typing import List

from config import Config
from database.collections import user, table_key
from models.other import Token
from models.user import UserAuth, User
from utils import auth


def insert_db(user_data: User) -> bool:
    if user_data._id is None:
        user_data._id = table_key.get_last_id('users').last_id
    return user.add_user(user_data)


def activate_user(email: str) -> bool:
    return user.activate(email)


def get_user_by_email(email: str) -> User:
    return user.get_user_by_email(email)


def login(user_data: UserAuth) -> Token:
    db_user = user.get_user_by_email(user_data.email)
    if db_user:
        if db_user.is_active is True:
            if auth.verify_password(user_data.password, db_user.hash_password):
                access_token_expires = timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = auth.create_access_token(
                    data={"sub": user_data.email}, expires_delta=access_token_expires
                )
                return Token(access_token=access_token, token_type="bearer")
    return None

def get_users_inactive_24_hours():
    return user.get_inactive(24)

def delete_user(id: int):
    return user.delete_user(id)

def delete_users(list_id: List[int]):
    return user.delete_users(list_id)