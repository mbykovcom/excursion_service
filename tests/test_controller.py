import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.other import Token
from utils.auth import get_hash_password
from controllers import user as user_service
from database.collections import user as user_coolection
from models.user import User, UserAuth


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

    def test_insert_db(self):
        result = user_service.insert_db(self.user)
        assert result is True

    def test_login_not_activate_user(self):
        jwt = user_service.login(UserAuth(email=self.user.email, password='Password_1'))
        assert jwt is None

    def test_activate_user(self):
        result = user_service.activate_user(self.user.email)
        assert result is True
        result = user_service.activate_user(self.user.email)
        return result is True

    def test_login(self):
        jwt = user_service.login(UserAuth(email=self.user.email, password='Password_1'))
        assert type(jwt) is Token
        TestUser.jwt = jwt
        jwt = user_service.login(UserAuth(email="error@email.ru", password='Password_1'))
        assert jwt is None
        jwt = user_service.login(UserAuth(email=self.user.email, password='ErrorPass'))
        assert jwt is None

    def test_get_users_inactive(self):
        user_1 = User('user_1@email.ru', get_hash_password('Password_1'), 'User')
        user_1.date_registration = datetime.now() - timedelta(hours=25)
        user_service.insert_db(user_1)
        users = user_service.get_users_inactive_24_hours()
        assert len(users) == 1
        assert users[0].email == user_1.email

    def test_delete_user(self):
        user_3 = User('user_3@email.ru', get_hash_password('Password_1'), 'User')
        user_service.insert_db(user_3)
        assert user_service.delete_user(3) is True

    def test_delete_users(self):
        assert user_service.delete_users([2]) is True


if __name__ == '__main__':
    unittest.main()
