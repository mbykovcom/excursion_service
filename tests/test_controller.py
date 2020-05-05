import copy
import unittest
from datetime import datetime, timedelta

from fastapi import HTTPException
from pytest import raises

from database import db
from database.connection import Database
from models.excursion_point import ExcursionPoint, ExcursionPointDetails
from models.listening import Listening
from models.track import Track
from models.user import User, UserAuth
from models.object import Object, Coordinates, ObjectUpdate
from models.excursion import Excursion, ExcursionUpdate, ExcursionOut
from models.other import Token, Statistics
from models.user_excurion import UserExcursion, UserExcursionsDetail, UserExcursionDetail

from utils.auth import get_hash_password
from controllers import user as user_service
from controllers import object as object_service
from controllers import excursion as excursion_service
from controllers import excursion_point as point_service
from controllers import track as track_service
from controllers import user_excursion as user_excursion_service
from controllers import statistics as statistics_service


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
        cls.obj = [Object(name='Object', description='Object`s description', location=Coordinates(lat=59.9390,
                                                                                                  lon=30.3157))]
        cls.jwt = None

    def teardown_class(cls):
        db = Database()
        objects = db.get_collection('objects')
        keys = db.get_collection('table_keys')
        objects.delete_many({})
        keys.delete_many({})

    def test_create_object(self):
        obj = object_service.create_object(self.obj[0])
        assert type(obj) is Object

    def test_delete_object(self):
        obj = object_service.delete_object(1)
        self.obj[0]._id = obj._id
        assert obj.name == self.obj[0].name

    def test_get_object_by_id(self):
        new_obj = object_service.create_object(self.obj[0])
        obj = object_service.get_object_by_id(2)
        assert obj.name == new_obj.name
        self.obj.append(obj)

    def test_get_objects(self):
        new_obj = copy.deepcopy(self.obj[0])
        new_obj.name = 'Object 3'
        object_service.create_object(new_obj)
        objects = object_service.get_objects()
        assert len(objects) == 2
        assert objects[1].name == new_obj.name
        self.obj.append(objects[1])

    def test_get_objects_by_list_id(self):
        objects = object_service.get_objects_by_list_id([self.obj[1]._id, self.obj[2]._id])
        assert len(objects) == 2
        assert objects[0].name == self.obj[1].name

    def test_update_object(self):
        update = ObjectUpdate(name='Update name')
        result = object_service.update_object(3, update)
        assert type(result) is Object
        assert result.name == update.name
        update.description = 'Update description'
        update.location = {'lat': 0.0, 'lon': 0.0}
        result = object_service.update_object(3, update)
        assert type(result) is Object
        assert result.name == update.name
        assert result.description == update.description
        assert type(result.location) is Coordinates
        assert result.location.lat == update.location['lat']
        assert result.location.lon == update.location['lon']
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
        points = db.get_collection('excursion_points')
        user_excursions = db.get_collection('user_excursions')
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        excursions.delete_many({})
        points.delete_many({})
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
        points = [ExcursionPoint(1, 1, 1, 1, 1), ExcursionPoint(1, 2, 2, 2, 2), ExcursionPoint(1, 3, 3, 3, 3)]
        point = point_service.create_excursion_point(points[0])
        point_service.create_excursion_point(points[1])
        point_service.create_excursion_point(points[2])
        excursion = excursion_service.delete_excursion(1)
        assert excursion.name == self.excursions[0].name
        points = point_service.get_excursion_points_by_excursion(1)
        assert len(points) == 0
        excursion = excursion_service.delete_excursion(10)
        assert excursion is None

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
        assert user_excursion._id == 1
        assert user_excursion.id_user == self.user._id
        assert user_excursion.id_excursion == self.excursions[2]._id
        assert user_excursion.id_last_point == 0
        assert user_excursion.is_active is True

        with raises(HTTPException):
            assert excursion_service.buy_excursion(self.excursions[2]._id, self.user._id)

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

    def test_get_tracks_by_list_id(self):
        tracks = track_service.get_tracks_by_list_id([self.tracks[1]._id, self.tracks[2]._id])
        assert len(tracks) == 2
        assert tracks[0].name == self.tracks[1].name

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


class TestExcursionPoints:

    def setup_class(cls):
        cls.points = [ExcursionPoint(1, 1, 1, 1)]
        cls.excursion = Excursion(name='Excursion', description='Excursion`s description', price=100.5)
        cls.obj = Object(name='Object', description='Object`s description', location=Coordinates(lat=59.9390,
                                                                                                 lon=30.3157))

    def teardown_class(cls):
        db = Database()
        points = db.get_collection('excursion_points')
        excursions = db.get_collection('excursions')
        objects = db.get_collection('objects')
        keys = db.get_collection('table_keys')
        points.delete_many({})
        excursions.delete_many({})
        objects.delete_many({})
        keys.delete_many({})

    def test_create_excursion_point(self):
        with raises(HTTPException) as e:
            assert point_service.create_excursion_point(ExcursionPoint(1, 2, 2, 2, 2))
        point = point_service.create_excursion_point(self.points[0])
        assert type(point) is ExcursionPoint
        assert point.id_excursion == self.points[0].id_excursion
        self.points[0]._id = point._id
        with raises(HTTPException) as e:
            assert point_service.create_excursion_point(self.points[0])
        with raises(HTTPException) as e:
            assert point_service.create_excursion_point(ExcursionPoint(1, 2, 2, 5, 3))

    def test_get_excursion_point_by_id(self):
        point = point_service.get_excursion_point_by_id(self.points[0]._id)
        assert type(point) is ExcursionPoint
        assert point._id == self.points[0]._id

    def test_get_excursion_points(self):
        self.points.append(ExcursionPoint(1, 2, 2, 2))
        self.points.append(ExcursionPoint(1, 3, 3, 3))
        self.points[1]._id = point_service.create_excursion_point(self.points[1])._id
        self.points[2]._id = point_service.create_excursion_point(self.points[2])._id
        points = point_service.get_excursion_points()
        assert len(points) == 3

    def test_get_excursion_points_by_excursion(self):
        points = point_service.get_excursion_points_by_excursion(self.points[0].id_excursion)
        assert len(points) == 3

    def test_update_excursion_point(self):
        point = point_service.update_excursion_point(self.points[2]._id)
        assert point.id_object == self.points[2].id_object
        assert point.id_track == self.points[2].id_track
        point = point_service.update_excursion_point(self.points[2]._id, 4)
        assert point.id_object == 4
        assert point.id_track == self.points[2].id_track
        point = point_service.update_excursion_point(self.points[2]._id, id_track=4)
        assert point.id_object == 4
        assert point.id_track == 4
        point = point_service.update_excursion_point(self.points[2]._id, 3, 3)
        assert point.id_object == self.points[2].id_object
        assert point.id_track == self.points[2].id_track

    def test_create_url_map_route(self):
        excursion = excursion_service.create_excursion(self.excursion)
        assert type(excursion) is Excursion

        obj_1 = object_service.create_object(self.obj)
        obj_2 = copy.deepcopy(self.obj)
        obj_2.location = Coordinates(lat=59.937, lon=30.3187)
        object_service.create_object(obj_2)
        obj_3 = copy.deepcopy(self.obj)
        obj_3.location = Coordinates(lat=59.938, lon=30.3167)
        object_service.create_object(obj_3)
        excursion.create_url_map_route()
        assert excursion.url_map_route is not None

    def test_check_track_in_excursion(self):
        result = point_service.check_track_in_excursion(1, 2)
        assert type(result) is ExcursionPoint
        result = point_service.check_track_in_excursion(1, 5)
        assert result is None

    def test_delete_excursion_point(self):
        point = point_service.delete_excursion_point(self.points[2]._id)
        assert point._id == self.points[2]._id
        point = point_service.delete_excursion_point(10)
        assert point is None


class TestUserExcursions:

    def setup_class(cls):
        cls.excursions = [Excursion(name='Excursion', description='Excursion`s description', price=100.5)]
        cls.excursions[0] = excursion_service.create_excursion(cls.excursions[0])
        cls.objects = [Object(name='Object', description='Object`s description',
                              location=Coordinates(lat=59.9390, lon=30.3157)),
                       Object(name='Object', description='Object`s description',
                              location=Coordinates(lat=59.937, lon=30.3187))]
        cls.objects[0] = object_service.create_object(cls.objects[0])
        cls.objects[1] = object_service.create_object(cls.objects[1])
        cls.tracks = [track_service.add_track(b'Track 1', 'Track 1'), track_service.add_track(b'Track 2', 'Track 2')]
        cls.points = [ExcursionPoint(cls.excursions[0]._id, cls.objects[0]._id, cls.tracks[0]._id, 1),
                      ExcursionPoint(cls.excursions[0]._id, cls.objects[1]._id, cls.tracks[1]._id, 2)]
        cls.points[0] = point_service.create_excursion_point(cls.points[0])
        cls.points[1] = point_service.create_excursion_point(cls.points[1])
        cls.user_excursions = [UserExcursion(1, 1, True)]

    def teardown_class(cls):
        db = Database()
        points = db.get_collection('excursion_points')
        excursions = db.get_collection('excursions')
        objects = db.get_collection('objects')
        tracks = db.get_collection('tracks')
        user_excursions = db.get_collection('user_excursions')
        keys = db.get_collection('table_keys')
        points.delete_many({})
        excursions.delete_many({})
        objects.delete_many({})
        tracks.delete_many({})
        user_excursions.delete_many({})
        keys.delete_many({})

    def test_create_user_excursion(self):
        user_excursion = user_excursion_service.create_user_excursion(1, self.excursions[0]._id)
        assert type(user_excursion) is UserExcursion
        assert user_excursion.id_user == 1
        assert user_excursion.is_active is True
        assert user_excursion.id_excursion == self.excursions[0]._id
        assert user_excursion.id_last_point == 0
        self.user_excursions[0] = user_excursion

    def test_deactivate_user_excursion(self):
        user_excursion = user_excursion_service.deactivate_user_excursion(self.user_excursions[0]._id)
        assert user_excursion.is_active is False
        user_excursion = user_excursion_service.deactivate_user_excursion(10)
        assert user_excursion is None

    def test_get_user_excursions_by_user_id(self):
        user_excursions = user_excursion_service.get_user_excursions_by_user_id(1)
        assert len(user_excursions) == 0
        self.user_excursions.append(user_excursion_service.create_user_excursion(1, self.excursions[0]._id))
        user_excursions = user_excursion_service.get_user_excursions_by_user_id(1)
        assert len(user_excursions) == 1
        assert user_excursions[0]._id == self.user_excursions[1]._id

    def test_get_user_excursions_by_id(self):
        user_excursion = user_excursion_service.get_user_excursion_by_id(self.user_excursions[1]._id)
        assert type(user_excursion) is UserExcursion
        assert user_excursion.id_user == 1
        assert user_excursion.is_active is True
        assert user_excursion.id_excursion == self.excursions[0]._id
        assert user_excursion.id_last_point == 0

    def test_update_last_point(self):
        self.user_excursions[1].id_last_point = 1
        user_excursion = user_excursion_service.update_last_point(self.user_excursions[1])
        assert user_excursion.id_last_point == 1

    def test_user_excursion_detail(self):
        user_excursions_detail = user_excursion_service.user_excursions_detail(self.user_excursions[1])
        assert type(user_excursions_detail) is UserExcursionDetail
        assert type(user_excursions_detail.excursion) is ExcursionOut
        assert type(user_excursions_detail.last_point) is ExcursionPointDetails

    def test_user_excursions_detail(self):
        user_excursion_detail = user_excursion_service.user_excursion_detail(self.user_excursions[1])
        assert type(user_excursion_detail) is UserExcursionsDetail
        assert type(user_excursion_detail.excursion) is ExcursionOut
        assert len(user_excursion_detail.list_point) == 2


class TestStatistics:
    def setup_class(cls):
        cls.now = datetime(2020, 5, 4, 18, 25)
        cls.users = [User('user1@email.ru', get_hash_password('Password_1'), 'User1', is_active=True,
                          date_registration=(cls.now - timedelta(minutes=21))),
                     User('user2@email.ru', get_hash_password('Password_1'), 'User2', is_active=True,
                          date_registration=(cls.now - timedelta(minutes=100))),
                     User('user3@email.ru', get_hash_password('Password_1'), 'User3', is_active=True,
                          date_registration=(datetime(2020, 5, 1, 18, 23))),
                     User('user4@email.ru', get_hash_password('Password_1'), 'User4', is_active=True,
                          date_registration=(datetime(2020, 4, 24, 10, 23))),
                     User('user5@email.ru', get_hash_password('Password_1'), 'User5', is_active=True,
                          date_registration=(datetime(2020, 1, 25, 22, 23)))]
        cls.users[0] = user_service.create_user(cls.users[0])
        cls.users[1] = user_service.create_user(cls.users[1])
        cls.users[2] = user_service.create_user(cls.users[2])
        cls.users[3] = user_service.create_user(cls.users[3])
        cls.users[4] = user_service.create_user(cls.users[4])

        cls.excursions = [Excursion(name='Excursion', description='Excursion`s description', price=100.5),
                          Excursion(name='Excursion', description='Excursion`s description', price=21.5)]
        cls.excursions[0] = excursion_service.create_excursion(cls.excursions[0])
        cls.excursions[1] = excursion_service.create_excursion(cls.excursions[1])

        cls.user_excursions = [UserExcursion(1, 1, True, date_added=(cls.now - timedelta(minutes=21))),
                               UserExcursion(1, 1, False, date_added=(cls.now - timedelta(minutes=100))),
                               UserExcursion(1, 1, False, date_added=(datetime(2020, 5, 1, 18, 23))),
                               UserExcursion(1, 2, True, date_added=(datetime(2020, 4, 24, 10, 23))),
                               UserExcursion(1, 2, True, date_added=(datetime(2020, 1, 25, 22, 23)))]
        cls.user_excursions[0] = db.add(cls.user_excursions[0])
        cls.user_excursions[1] = db.add(cls.user_excursions[1])
        cls.user_excursions[2] = db.add(cls.user_excursions[2])
        cls.user_excursions[3] = db.add(cls.user_excursions[3])
        cls.user_excursions[4] = db.add(cls.user_excursions[4])

        cls.listening = [Listening(1, 1, date_listening=cls.now - timedelta(minutes=7)),
                         Listening(2, 1, date_listening=cls.now - timedelta(hours=22)),
                         Listening(3, 2, date_listening=cls.now - timedelta(days=10))]
        cls.listening[0] = statistics_service.add_listening(cls.listening[0])
        cls.listening[1] = statistics_service.add_listening(cls.listening[1])
        cls.listening[2] = statistics_service.add_listening(cls.listening[2])

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        excursions = db.get_collection('excursions')
        user_excursions = db.get_collection('user_excursions')
        listening = db.get_collection('listening')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        excursions.delete_many({})
        user_excursions.delete_many({})
        listening.delete_many({})
        keys.delete_many({})

    def test_specify_period(self):
        period = statistics_service.specify_period(None, None)
        assert period[0].day == 4
        assert period[1].day == 10

        now = datetime.now()
        start = now - timedelta(days=3)
        end = now + timedelta(days=10)
        period = statistics_service.specify_period(start, end)
        assert period[0].day == start.day
        assert period[1].day == end.day

        period = statistics_service.specify_period(None, end)
        day = now.isoweekday()
        assert period[0].day == (now - timedelta(days=day - 1)).day
        assert period[1].day == end.day

        period = statistics_service.specify_period(start, None)
        assert period[0].day == start.day
        assert period[1].day == now.day

    def test_generating_segments(self):
        start = self.now - timedelta(minutes=12)
        end = self.now

        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments is None

        start = self.now - timedelta(minutes=50)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments[0] == 'minutes'
        assert segments[1][1][0] == start
        assert segments[1][4][1] == end
        assert len(segments[1]) == 4

        start = self.now - timedelta(hours=7)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments[0] == 'hours'
        assert segments[1][1][0] == start
        assert segments[1][7][1] == end
        assert len(segments[1]) == 7

        start = self.now - timedelta(days=7)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments[0] == 'days'
        assert segments[1][1][0] == datetime(year=start.year, month=start.month, day=start.day)
        assert segments[1][7][1] == datetime(year=end.year, month=end.month, day=end.day) - timedelta(microseconds=1)
        assert len(segments[1]) == 7

        start = self.now - timedelta(days=31)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments[0] == 'weeks'
        assert segments[1][1][0] == datetime(year=start.year, month=start.month, day=start.day)
        assert segments[1][5][1] == datetime(year=start.year, month=start.month, day=start.day) + timedelta(days=7*5) \
               - timedelta(microseconds=1)
        assert len(segments[1]) == 5

        start = self.now - timedelta(days=365)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments is None

        start = datetime(2019, 5, 1)
        end = datetime(2020, 4, 30)
        period = statistics_service.specify_period(start, end)
        segments = statistics_service.generating_segments(period)
        assert segments[0] == 'months'
        assert segments[1][1][0] == start
        assert segments[1][12][1] == end + timedelta(days=1)\
               - timedelta(microseconds=1)
        assert len(segments[1]) == 12

    def test_get_statistics_users(self):
        start = self.now - timedelta(minutes=50)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_users(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'minutes'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 1
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(hours=2)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_users(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'hours'
        assert len(statistics.data) == 2
        assert statistics.data[1] == 1
        assert statistics.data[2] == 1

        start = self.now - timedelta(days=4)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_users(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'days'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 1
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(days=28)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_users(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'weeks'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 0
        assert statistics.data[3] == 1
        assert statistics.data[4] == 1

        start = datetime(2019, 5, 1)
        end = datetime(2020, 4, 30)
        period = statistics_service.specify_period(start, end)
        statistics = statistics_service.get_statistics_users(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'months'
        assert len(statistics.data) == 12
        assert statistics.data[9] == 1
        assert statistics.data[12] == 1

    def test_get_statistics_excursions(self):
        start = self.now - timedelta(minutes=50)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_excursions(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'minutes'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 1
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(hours=2)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_excursions(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'hours'
        assert len(statistics.data) == 2
        assert statistics.data[1] == 1
        assert statistics.data[2] == 1

        start = self.now - timedelta(days=4)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_excursions(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'days'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 1
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(days=28)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_excursions(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'weeks'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 0
        assert statistics.data[3] == 1
        assert statistics.data[4] == 1

        start = datetime(2019, 5, 1)
        end = datetime(2020, 4, 30)
        period = statistics_service.specify_period(start, end)
        statistics = statistics_service.get_statistics_excursions(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'months'
        assert len(statistics.data) == 12
        assert statistics.data[9] == 1
        assert statistics.data[12] == 1

    def test_get_statistics_listening(self):
        start = self.now - timedelta(minutes=50)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_listening(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'minutes'
        assert len(statistics.data) == 4
        assert statistics.data[3] == 1

        start = self.now - timedelta(hours=2)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_listening(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'hours'
        assert len(statistics.data) == 2
        assert statistics.data[2] == 1

        start = self.now - timedelta(days=4)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_listening(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'days'
        assert len(statistics.data) == 4
        assert statistics.data[4] == 1

        start = self.now - timedelta(days=28)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_listening(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'weeks'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 0
        assert statistics.data[3] == 1
        assert statistics.data[4] == 1

        start = datetime(2019, 5, 1)
        end = datetime(2020, 4, 30)
        period = statistics_service.specify_period(start, end)
        statistics = statistics_service.get_statistics_listening(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'months'
        assert len(statistics.data) == 12
        assert statistics.data[12] == 1

    def test_get_statistics_sales(self):
        start = self.now - timedelta(minutes=50)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_sales(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'minutes'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == self.excursions[0].price
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(hours=2)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_sales(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'hours'
        assert len(statistics.data) == 2
        assert statistics.data[1] == self.excursions[0].price
        assert statistics.data[2] == self.excursions[0].price

        start = self.now - timedelta(days=4)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_sales(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'days'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == self.excursions[0].price
        assert statistics.data[3] == 0
        assert statistics.data[4] == 0

        start = self.now - timedelta(days=28)
        period = statistics_service.specify_period(start, self.now)
        statistics = statistics_service.get_statistics_sales(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'weeks'
        assert len(statistics.data) == 4
        assert statistics.data[1] == 0
        assert statistics.data[2] == 0
        assert statistics.data[3] == self.excursions[1].price
        assert statistics.data[4] == self.excursions[0].price

        start = datetime(2019, 5, 1)
        end = datetime(2020, 4, 30)
        period = statistics_service.specify_period(start, end)
        statistics = statistics_service.get_statistics_sales(period)
        assert type(statistics) is Statistics
        assert statistics.type == 'months'
        assert len(statistics.data) == 12
        assert statistics.data[9] == self.excursions[1].price
        assert statistics.data[12] == self.excursions[1].price


if __name__ == '__main__':
    unittest.main()
