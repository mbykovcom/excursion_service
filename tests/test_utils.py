import unittest
from datetime import timedelta
from time import sleep

from fastapi import HTTPException
from pytest import raises

from database.connection import Database
from models.user import User
from utils import auth
from controllers import user as user_service
from utils.auth import get_hash_password


class TestUtils:

    def setup_class(cls):
        cls.user = {'email': 'user@email.ru', 'password': 'Password_1'}
        user_service.create_user(User(email=cls.user['email'], hash_password=get_hash_password(cls.user['password']),
                                      name='User'))
        user_service.activate_user(cls.user['email'])
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        keys.delete_many({})

    def test_checking_password(self):
        assert auth.checking_password_complexity('password') == 'Easy'
        assert auth.checking_password_complexity('NewPassword') == 'Medium'
        assert auth.checking_password_complexity('NewPassword2') == 'Hard'
        assert auth.checking_password_complexity('NewPassword_3') == 'Hard'

    def test_create_access_token(self):
        TestUtils.jwt = auth.create_access_token(data={"sub": self.user['email']}, expires_delta=timedelta(minutes=15))
        assert self.jwt is not None

    def test_authentication(self):
        jwt = auth.create_access_token(data={"sub": self.user['email']}, expires_delta=timedelta(microseconds=1))
        sleep(1)
        user = auth.authentication(self.jwt)
        assert user.email == self.user['email']
        assert user.is_active is True
        with raises(HTTPException):
            assert auth.authentication(jwt)




if __name__ == '__main__':
    unittest.main()
