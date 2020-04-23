import copy
import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.object import Object, Coordinates
from models.other import Token
from utils.auth import get_hash_password
from controllers import user as user_service
from controllers import object as object_service
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

    def test_create_user(self):
        result = user_service.create_user(self.user)
        assert type(result) is User

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
        user_service.create_user(user_1)
        users = user_service.get_users_inactive_24_hours()
        assert len(users) == 1
        assert users[0].email == user_1.email

    def test_delete_user(self):
        user_3 = User('user_3@email.ru', get_hash_password('Password_1'), 'User')
        user_service.create_user(user_3)
        assert user_service.delete_user(3).email == user_3.email

    def test_delete_users(self):
        assert user_service.delete_users([2]) is True


class TestObject:

    def setup_class(cls):
        cls.obj = Object(name='Object', description='Object`s description', location=Coordinates(lat=59.9390,
                                                                                                 lon=30.3157))
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        objects = db.get_collection('objects')
        keys = db.get_collection('table_keys')
        objects.delete_many({})
        keys.delete_many({})

    def test_create_object(self):
        obj = object_service.create_object(self.obj)
        assert type(obj) is Object

    def test_delete_object(self):
        obj = object_service.delete_object(1)
        assert obj.name == self.obj.name

    def test_get_object_by_id(self):
        new_obj = object_service.create_object(self.obj)
        obj = object_service.get_object_by_id(2)
        assert obj.name == new_obj.name

    def test_get_objects(self):
        obj_copy = copy.deepcopy(self.obj)
        obj_copy.name = 'Object 2'
        object_service.create_object(obj_copy)
        objects = object_service.get_objects()
        assert len(objects) == 2
        assert objects[1].name == obj_copy.name


if __name__ == '__main__':
    unittest.main()
