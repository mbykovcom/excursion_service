import copy
import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.excursion import Excursion
from models.excursion_point import ExcursionPoint
from models.object import Object, Coordinates
from models.other import TableKey
from models.track import Track
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
        objects = db.get_collection('objects')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        objects.delete_many({})
        keys.delete_many({})

    def test_add(self):
        result = db.add(self.user)
        assert type(result) is User

    def test_delete(self):
        user_2 = User('user_2@email.ru', get_hash_password('Password_1'), 'User')
        db.add(user_2)
        assert db.delete(2, 'users') is True

    def test_update_item(self):
        update = copy.deepcopy(self.user)
        update._id = 1
        update.name = 'Updated name'
        update.email = 'update@email.ru'
        result = db.update_item(update)
        assert result is True

    def test_get_data_by_id(self):
        user = db.get_data_by_id(1, 'users')
        assert type(user) is User
        assert user._id == self.user._id

    def test_get_all_items(self):
        users = db.get_all_items('users')
        assert type(users) is list
        assert len(users) == 1
        assert type(users[0]) is User

    def test_get_items_by_list(self):
        objects_in_db = [Object('Object 1', 'Description 1', Coordinates(lat=38.12, lon=55.43), _id=1),
                         Object('Object 2', 'Description 2', Coordinates(lat=38.99, lon=55.01), _id=2)]
        db.add(objects_in_db[0])
        db.add(objects_in_db[1])
        list_id = [1, 2]
        objects = db.get_items_by_list_id('objects', list_id)
        assert objects_in_db[0].name == objects[0].name
        assert objects_in_db[1].name == objects[1].name

    def test_delete_items_by_list_id(self):
        assert db.delete_items_by_list_id([1, 2], 'objects') is True


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
        assert db.delete_items_by_list_id([2, 3], 'users') is True


class TestExcursion:
    def setup_class(cls):
        cls.excursion = Excursion(name='Excursion', description='Excursion`s description', price=100.5)
        db.add(cls.excursion)
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        excursions = db.get_collection('excursions')
        keys = db.get_collection('table_keys')
        excursions.delete_many({})
        keys.delete_many({})

    def test_get_excursions(self):
        new_excursions = copy.deepcopy(self.excursion)
        new_excursions.name = 'Excursion 2'
        new_excursions.url_map_route = 'url'
        db.add(new_excursions)
        excursions = db.get_excursions()
        assert len(excursions) == 1
        assert excursions[0].name == new_excursions.name
        assert excursions[0].url_map_route == new_excursions.url_map_route

    def test_update_url(self):
        self.excursion.url_map_route = 'map_map'
        assert db.update_url(self.excursion) is True


class TestTrack:
    def setup_class(cls):
        cls.track = Track(1, 'Track')
        db.add(cls.track)
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        tracks = db.get_collection('tracks')
        keys = db.get_collection('table_keys')
        tracks.delete_many({})
        keys.delete_many({})

    def test_get_track_by_name(self):
        track = db.get_track_by_name(self.track.name)
        assert type(track) is Track
        assert track.name == self.track.name


class TestExcursionPoint:
    def setup_class(cls):
        cls.points = [ExcursionPoint(1, 1, 1, 1, 1), ExcursionPoint(1, 2, 2, 2, 2), ExcursionPoint(1, 3, 3, 3, 3)]
        db.add(cls.points[0])
        db.add(cls.points[1])
        db.add(cls.points[2])

    def teardown_class(cls):
        db = Database()
        points = db.get_collection('excursion_points')
        keys = db.get_collection('table_keys')
        points.delete_many({})
        keys.delete_many({})

    def test_get_points(self):
        points = db.get_points(1)
        assert len(points) == 3
        assert points[0].sequence_number == self.points[0].sequence_number


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
