import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.other import TableKey
from utils.auth import get_hash_password
from database import db
from models.user import User


class TestBase:

    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        keys.delete_many({})

    def test_add(self):
        result = db.add(self.user)
        assert type(result) is User

    def test_delete(self):
        user_2 = User('user_2@email.ru', get_hash_password('Password_1'), 'User')
        db.add(user_2)
        assert db.delete(2, 'users') is True

    def test_get_data_by_id(self):
        user = db.get_data_by_id(1, 'users')
        assert type(user) is User
        assert user._id == self.user._id

    def test_get_all_items(self):
        users = db.get_all_items('users')
        assert type(users) is list
        assert len(users) == 1
        assert type(users[0]) is User


class TestUser:
    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        db.add(cls.user)
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        keys.delete_many({})

    def test_get_user_by_email(self):
        user = db.get_user_by_email(self.user.email)
        assert type(user) is User
        assert user.email == self.user.email
        TestBase.user._id = user._id

    def test_activate_user(self):
        result = db.activate_user(self.user.email)
        return result is True

    def test_get_users_inactive(self):
        user_2 = User('user_2@email.ru', get_hash_password('Password_1'), 'User')
        user_2.date_registration = datetime.now() - timedelta(hours=25)
        db.add(user_2)
        user_3 = User('user_3@email.ru', get_hash_password('Password_1'), 'User')
        db.add(user_3)
        users = db.get_inactive()
        assert len(users) == 2
        users = db.get_inactive(24)
        assert len(users) == 1
        assert users[0].email == user_2.email

    def test_delete_users(self):
        assert db.delete_users([2, 3]) is True


class TestTableKey:
    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        keys = db.get_collection('table_keys')
        keys.delete_many({})

    def test_add_key(self):
        key = db.add_key('users')
        assert type(key) is TableKey
        assert key.table == 'users'
        assert key.last_id == 1

    def test_get_last_id(self):
        key = db.get_last_id('users')
        assert type(key) is TableKey
        assert key.table == 'users'
        assert key.last_id == 1


if __name__ == '__main__':
    unittest.main()
