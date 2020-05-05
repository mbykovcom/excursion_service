import copy
import unittest
from datetime import datetime, timedelta

from database.connection import Database
from models.excursion import Excursion
from models.excursion_point import ExcursionPoint
from models.listening import Listening
from models.object import Object, Coordinates
from models.other import TableKey
from models.track import Track
from models.user_excurion import UserExcursion
from utils.auth import get_hash_password
from database import db
from models.user import User


class TestBase:

    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')

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
        cls.points[0] = db.add(cls.points[0])
        cls.points[1] = db.add(cls.points[1])
        cls.points[2] = db.add(cls.points[2])

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

    def test_check_track_in_excursion(self):
        point = db.check_track_in_excursion(1, 1)
        assert type(point) is ExcursionPoint
        point = db.check_track_in_excursion(1, 10)
        assert point is None


class TestUserExcursion:
    def setup_class(cls):
        cls.user_excursions = [UserExcursion(1, 1, True)]
        cls.user_excursions[0] = db.add(cls.user_excursions[0])

    def teardown_class(cls):
        db = Database()
        user_excursions = db.get_collection('user_excursions')
        keys = db.get_collection('table_keys')
        user_excursions.delete_many({})
        keys.delete_many({})

    def test_get_user_excursion_by_user_id(self):
        user_excursions = db.get_user_excursion_by_user_id(1)
        assert len(user_excursions) == 1
        assert type(user_excursions[0]) is UserExcursion
        assert user_excursions[0].id_user == 1

    def test_deactivating_user_excursion(self):
        result = db.deactivating_user_excursion(self.user_excursions[0]._id)
        assert result is True
        result = db.deactivating_user_excursion(self.user_excursions[0]._id)
        assert result is False

    def test_check_user_excursion_is_active(self):
        self.user_excursions.append(UserExcursion(2, 2, True))
        self.user_excursions[1] = db.add(self.user_excursions[1])
        user_excursion = db.check_user_excursion_is_active(self.user_excursions[1].id_excursion)
        assert type(user_excursion) is UserExcursion
        assert user_excursion.id_excursion == self.user_excursions[1].id_excursion

        result = db.deactivating_user_excursion(self.user_excursions[1]._id)
        assert result is True

        user_excursion = db.check_user_excursion_is_active(self.user_excursions[1].id_excursion)
        assert user_excursion is None

    def test_get_expired_user_excursions(self):
        self.user_excursions.append(UserExcursion(3, 3, True, date_added=datetime.now() - timedelta(days=31)))
        self.user_excursions[2] = db.add(self.user_excursions[2])
        self.user_excursions.append(UserExcursion(4, 4, True, date_added=datetime.now() - timedelta(days=30)))
        self.user_excursions[3] = db.add(self.user_excursions[3])

        user_excursions = db.get_expired_user_excursions(31)
        assert len(user_excursions) == 1


class TestStatistics:
    def setup_class(cls):
        cls.now = datetime.now()
        cls.users = [User('user1@email.ru', get_hash_password('Password_1'), 'User1', is_active=True,
                          date_registration=(cls.now - timedelta(days=31))),
                     User('user2@email.ru', get_hash_password('Password_1'), 'User2', is_active=True,
                          date_registration=(cls.now - timedelta(days=10))),
                     User('user3@email.ru', get_hash_password('Password_1'), 'User3', is_active=True,
                          date_registration=(cls.now - timedelta(days=1)))]
        cls.users[0] = db.add(cls.users[0])
        cls.users[1] = db.add(cls.users[1])
        cls.users[2] = db.add(cls.users[2])

        cls.user_excursions = [UserExcursion(1, 1, True),
                               UserExcursion(2, 1, True, date_added=cls.now - timedelta(days=22)),
                               UserExcursion(3, 2, True, date_added=cls.now - timedelta(days=10))]
        cls.user_excursions[0] = db.add(cls.user_excursions[0])
        cls.user_excursions[1] = db.add(cls.user_excursions[1])
        cls.user_excursions[2] = db.add(cls.user_excursions[2])

        cls.listening = [Listening(1, 1, date_listening=cls.now - timedelta(minutes=2)),
                         Listening(2, 1, date_listening=cls.now - timedelta(days=22)),
                         Listening(3, 2, date_listening=cls.now - timedelta(days=10))]
        cls.listening[0] = db.add(cls.listening[0])
        cls.listening[1] = db.add(cls.listening[1])
        cls.listening[2] = db.add(cls.listening[2])

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        user_excursions = db.get_collection('user_excursions')
        listening = db.get_collection('listening')
        users.delete_many({})
        keys.delete_many({})
        user_excursions.delete_many({})
        listening.delete_many({})

    def test_get_user_statistics(self):
        count = db.get_user_statistics(self.now - timedelta(days=5), self.now)
        assert count == 1
        count = db.get_user_statistics(self.now - timedelta(days=11), self.now)
        assert count == 2
        count = db.get_user_statistics(self.now - timedelta(days=32), self.now - timedelta(days=5))
        assert count == 2

    def test_get_excursion_statistics(self):
        count = db.get_excursion_statistics(self.now - timedelta(days=5), self.now)
        assert count == 1
        count = db.get_excursion_statistics(self.now - timedelta(days=11), self.now)
        assert count == 2
        count = db.get_excursion_statistics(self.now - timedelta(days=32), self.now - timedelta(days=5))
        assert count == 2

    def test_get_sales_statistics(self):
        excursions = db.get_sales_statistics(self.now - timedelta(days=31), self.now)
        assert len(excursions) == 2
        assert excursions[0]['_id'] == 1
        assert excursions[0]['count'] == 2
        assert excursions[1]['_id'] == 2
        assert excursions[1]['count'] == 1

    def test_get_listening_statistics(self):
        count = db.get_listening_statistics(self.now - timedelta(minutes=50), self.now)
        assert count == 1
        count = db.get_listening_statistics(self.now - timedelta(days=11), self.now)
        assert count == 2
        count = db.get_listening_statistics(self.now - timedelta(days=32), self.now - timedelta(days=5))
        assert count == 2


class TestTableKey:
    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')

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
