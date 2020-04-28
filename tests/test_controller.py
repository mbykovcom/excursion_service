import copy
import unittest
from datetime import datetime, timedelta

from fastapi import HTTPException
from pytest import raises

from database.connection import Database
from models.track import Track
from models.user import User, UserAuth
from models.object import Object, Coordinates, ObjectUpdate
from models.excursion import Excursion, ExcursionUpdate
from models.other import Token

from utils.auth import get_hash_password
from controllers import user as user_service
from controllers import object as object_service
from controllers import excursion as excursion_service
from controllers import track as track_service


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
        obj_copy.name = 'Object 3'
        object_service.create_object(obj_copy)
        objects = object_service.get_objects()
        assert len(objects) == 2
        assert objects[1].name == obj_copy.name

    def test_update_object(self):
        update = ObjectUpdate(name='Update name')
        result = object_service.update_object(3, update)
        assert type(result) is Object
        assert result.name == update.name
        update.description = 'Update description'
        update.location = Coordinates(lat=0.0, lon=0.0)
        result = object_service.update_object(3, update)
        assert type(result) is Object
        assert result.name == update.name
        assert result.description == update.description
        assert result.location == update.location
        result = object_service.update_object(10, update)
        assert result is None


class TestExcursion:
    def setup_class(cls):
        cls.excursions = [Excursion(name='Excursion', description='Excursion`s description', price=100.5)]
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.user._id = user_service.create_user(cls.user)._id

    def teardown_class(cls):
        db = Database()
        excursions = db.get_collection('excursions')
        user_excursions = db.get_collection('user_excursions')
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        excursions.delete_many({})
        user_excursions.delete_many({})
        keys.delete_many({})
        users.delete_many({})

    def test_create_excursion(self):
        excursion = excursion_service.create_excursion(self.excursions[0])
        assert type(excursion) is Excursion
        assert excursion._id == 1
        assert excursion.name == self.excursions[0].name
        assert excursion.description == self.excursions[0].description
        assert excursion.price == self.excursions[0].price
        assert excursion.url_map_route is None
        self.excursions[0]._id = excursion._id

    def test_delete_excursion(self):
        excursion = excursion_service.delete_excursion(1)
        assert excursion.name == self.excursions[0].name

    def test_get_excursion_by_id(self):
        self.excursions.append(Excursion(name='Excursion 2', description='Description 2', price=200.5))
        self.excursions[1]._id = excursion_service.create_excursion(self.excursions[1])._id
        excursion = excursion_service.get_excursion_by_id(self.excursions[1]._id)
        assert excursion.name == self.excursions[1].name

    def test_get_excursions(self):
        self.excursions.append(Excursion(name='Excursion 3', description='Description 3', price=300.5,
                                         url_map_route='URL'))
        self.excursions[2]._id = excursion_service.create_excursion(self.excursions[2])._id
        excursions = excursion_service.get_excursions('admin')
        assert len(excursions) == 2
        assert excursions[0].name == self.excursions[1].name
        assert excursions[0].url_map_route == self.excursions[1].url_map_route
        excursions = excursion_service.get_excursions('user')
        assert len(excursions) == 1
        assert excursions[0].name == self.excursions[2].name
        assert excursions[0].url_map_route == self.excursions[2].url_map_route

    def test_update_excursion(self):
        update = ExcursionUpdate()
        result = excursion_service.update_excursion(self.excursions[2]._id, update)
        assert type(result) is Excursion
        assert result.name == self.excursions[2].name
        assert result.description == self.excursions[2].description
        assert result.price == self.excursions[2].price
        update.name = 'Update name'
        result = excursion_service.update_excursion(self.excursions[2]._id, update)
        assert type(result) is Excursion
        assert result.name == update.name
        update.description = 'Update description'
        update.price = 1010.99
        result = excursion_service.update_excursion(self.excursions[2]._id, update)
        assert type(result) is Excursion
        assert result.name == update.name
        assert result.description == update.description
        assert result.price == update.price
        self.excursions[2].name = update.name
        self.excursions[2].description = update.description
        self.excursions[2].price = update.price
        result = excursion_service.update_excursion(10, update)
        assert result is None

    def test_buy_excursion(self):
        user_excursion = excursion_service.buy_excursion(self.excursions[2]._id, self.user._id)
        print(user_excursion)
        assert user_excursion._id == 1
        assert user_excursion.id_user == self.user._id
        assert user_excursion.id_excursion == self.excursions[2]._id
        assert user_excursion.id_last_point == 0
        assert user_excursion.is_active is True

        user_excursion = excursion_service.buy_excursion(10, self.user._id)
        assert user_excursion is None


class TestTrack:
    def setup_class(cls):
        cls.tracks = [Track('Track')]
        cls.track_binary = b'track'
        cls.tracks_in_storage = {'track_data': b'track data', 'name': 'Track Name'}

    def teardown_class(cls):
        db = Database()
        tracks = db.get_collection('tracks')
        keys = db.get_collection('table_keys')
        tracks.delete_many({})
        keys.delete_many({})

    def test_add_track_in_cloud(self):
        result = track_service.add_track_in_cloud(self.tracks_in_storage['track_data'],
                                                  self.tracks_in_storage['name'])
        assert result is True

    def test_get_track_from_cloud(self):
        result = track_service.get_track_from_cloud(self.tracks_in_storage['name'])
        assert type(result) is bytes
        assert result == self.tracks_in_storage['track_data']

    def test_delete_track_form_cloud(self):
        result = track_service.delete_track_form_cloud(self.tracks_in_storage['name'])
        assert result is True

    def test_add_track(self):
        self.tracks[0] = track_service.add_track(self.track_binary, self.tracks[0].name)
        assert type(self.tracks[0]) is Track
        assert self.tracks[0]._id == 1
        assert self.tracks[0].name == self.tracks[0].name
        assert self.tracks[0].url is not None
        with raises(HTTPException):
            assert track_service.add_track(self.track_binary, self.tracks[0].name)

    def test_delete_track(self):
        track = track_service.delete_track(self.tracks[0]._id)
        assert track.name == self.tracks[0].name
        track = track_service.delete_track(10)
        assert track is None

    def test_get_track_by_id(self):
        self.tracks.append(Track('Track 2'))
        self.tracks[1] = track_service.add_track(self.track_binary, self.tracks[1].name)
        track = track_service.get_track_by_id(self.tracks[1]._id)
        assert track.name == self.tracks[1].name
        track = track_service.delete_track(10)
        assert track is None

    def test_get_tracks(self):
        self.tracks.append(Track('Track 3'))
        self.tracks[2] = track_service.add_track(self.track_binary, self.tracks[2].name)
        tracks = track_service.get_tracks()
        assert len(tracks) == 2
        assert tracks[0].name == self.tracks[1].name
        assert tracks[0].url == self.tracks[1].url

    def test_update_track(self):
        result = track_service.update_track(self.tracks[1]._id)
        assert result is None

        with raises(HTTPException):
            assert track_service.update_track(10, b'Update', 'Update')

        result = track_service.update_track(self.tracks[1]._id, b'Update', 'Update')
        assert type(result) is Track
        assert result.name == 'Update'
        assert result.url != self.tracks[1].url
        self.tracks[1].name = result.name
        self.tracks[1].url = result.url

        result = track_service.update_track(self.tracks[1]._id, b'Update 2')
        assert type(result) is Track
        assert result.name == self.tracks[1].name
        assert result.url == self.tracks[1].url

        result = track_service.update_track(self.tracks[1]._id, name='Update 2')
        assert type(result) is Track
        assert result.name == 'Update 2'
        assert result.url != self.tracks[1].url
        self.tracks[1].name = result.name
        self.tracks[1].url = result.url


if __name__ == '__main__':
    unittest.main()
