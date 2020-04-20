import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.other import TableKey
from utils.auth import get_hash_password
from database.collections import user as user_collection
from database.collections import table_key as key_collection
from models.user import User


class TestUser:

    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        keys.delete_many({})

    def test_add_user(self):
        result = user_collection.add_user(self.user)
        assert result is True

    def test_get_user_by_email(self):
        user = user_collection.get_user_by_email(self.user.email)
        assert type(user) is User
        assert user.email == self.user.email
        TestUser.user._id = user._id

    def test_get_user_by_id(self):
        user = user_collection.get_user_by_id(self.user._id)
        assert type(user) is User
        assert user._id == self.user._id

    def test_activate_user(self):
        result = user_collection.activate(self.user.email)
        return result is True

    def test_get_users_inactive(self):
        user_1 = User('user_1@email.ru', get_hash_password('Password_1'), 'User')
        user_1.date_registration = datetime.now() - timedelta(hours=25)
        user_collection.add_user(user_1)
        user_2 = User('user_2@email.ru', get_hash_password('Password_1'), 'User')
        user_collection.add_user(user_2)
        users = user_collection.get_inactive()
        assert len(users) == 2
        users = user_collection.get_inactive(24)
        assert len(users) == 1
        assert users[0].email == user_1.email

    def test_delete_user(self):
        user_3 = User('user_3@email.ru', get_hash_password('Password_1'), 'User')
        user_collection.add_user(user_3)
        assert user_collection.delete_user(4) is True

    def test_delete_users(self):
        assert user_collection.delete_users([2, 3]) is True


class TestTableKey:
    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        keys = db.get_collection('table_keys')
        keys.delete_many({})

    def test_add(self):
        key = key_collection.add('users')
        assert type(key) is TableKey
        assert key.table == 'users'
        assert key.last_id == 1

    def test_get_last_id(self):
        key = key_collection.get_last_id('users')
        assert type(key) is TableKey
        assert key.table == 'users'
        assert key.last_id == 1


if __name__ == '__main__':
    unittest.main()
