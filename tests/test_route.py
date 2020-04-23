from datetime import timedelta
from time import sleep

from starlette.testclient import TestClient

from app import app
from config import Config
from controllers.user import login, create_user
from database.connection import Database
from models.object import Object, Coordinates
from models.user import User, UserAuth
from utils import auth
from utils.auth import get_hash_password

client = TestClient(app)


class TestAuth:

    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.headers = None

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        keys.delete_many({})

    def test_registration(self):
        json = {'email': self.user.email, 'password': 'Password_1', 'name': self.user.name}
        response = client.post('/registration', json=json)
        assert response.status_code == 201
        assert response.json() == {"id": 1,
                                   "email": self.user.email,
                                   "name": self.user.name,
                                   "role": "user",
                                   "date_registration": response.json()['date_registration']}
        TestAuth.user._id = response.json()['id']

        json = {'email': self.user.email, 'password': 'password', 'name': self.user.name}
        response = client.post('/registration', json=json)
        assert response.status_code == 400
        assert response.json() == {'detail': 'Your password is too simple. The password must contain uppercase and '
                                             'lowercase letters, as well as numbers and special characters'}

    def test_confirmation_registration(self):
        expired_token = auth.create_access_token(data={"sub": self.user.email},
                                                 expires_delta=timedelta(microseconds=1)).decode()
        access_token = auth.create_access_token(data={"sab": self.user.email},
                                                expires_delta=timedelta(
                                                    hours=Config.REGISTRATION_EXPIRE_HOURS)).decode()

        response = client.post(f'/registration/{access_token}')
        assert response.status_code == 400
        assert response.json() == {'detail': 'Invalid token'}

        sleep(1)
        response = client.post(f'/registration/{expired_token}')
        assert response.status_code == 404
        assert response.json() == {'detail': 'Invalid url'}

        access_token = auth.create_access_token(data={"sub": self.user.email}, expires_delta=timedelta(
            hours=Config.REGISTRATION_EXPIRE_HOURS)).decode()
        response = client.post(f'/registration/{access_token}')
        assert response.status_code == 200
        assert response.json() == {'detail': 'The user activated'}

        response = client.post(f'/registration/{access_token}')
        assert response.status_code == 400
        assert response.json() == {'detail': 'Invalid token'}

        access_token = auth.create_access_token(data={"sub": self.user.email},
                                                expires_delta=timedelta(
                                                    hours=Config.REGISTRATION_EXPIRE_HOURS)).decode()
        response = client.post(f'/registration/{access_token}')
        assert response.status_code == 400
        assert response.json() == {'detail': 'Invalid token'}

    def test_login(self):
        json = {'email': self.user.email, 'password': 'Password_1'}
        response = client.post('/login', json=json)
        assert response.status_code == 200
        assert list(response.json().keys()) == ['access_token', 'token_type']
        json['email'] = 'error@email.ru'
        response = client.post('/login', json=json)
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}


class TestObject:

    def setup_class(cls):
        cls.admin = User(email='admin@email.ru', hash_password=get_hash_password('AdminPassword_1'), name='Admin',
                         role='admin',
                         is_active=True)
        create_user(cls.admin)
        cls.headers = {'jwt': login(UserAuth(email='admin@email.ru', password='AdminPassword_1')).access_token}

        cls.obj = Object(name='Object', description='Object`s description', location=Coordinates(lat=59.9390,
                                                                                                 lon=30.3157))

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        objects = db.get_collection('objects')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        objects.delete_many({})
        keys.delete_many({})

    def test_create_object(self):
        json = {'name': self.obj.name, 'description': self.obj.description, 'location': {'lat': self.obj.location.lat,
                                                                                         'lon': self.obj.location.lon}}
        response = client.post('/object', json=json, headers=self.headers)
        assert response.status_code == 201
        assert response.json() == {"id": 1,
                                   "name": self.obj.name,
                                   "description": self.obj.description,
                                   "location": {'lat': self.obj.location.lat, 'lon': self.obj.location.lon}}
        TestObject.obj._id = response.json()['id']

    def test_get_objects(self):
        response = client.get('/object', headers=self.headers)
        assert response.status_code == 200
        assert response.json() == [
            {"id": 1,
             "name": self.obj.name,
             "description": self.obj.description,
             "location": {'lat': self.obj.location.lat, 'lon': self.obj.location.lon}}
        ]

    def test_get_object_by_id(self):
        response = client.get('/object/1', headers=self.headers)
        assert response.status_code == 200
        assert response.json() == {"id": 1,
                                   "name": self.obj.name,
                                   "description": self.obj.description,
                                   "location": {'lat': self.obj.location.lat, 'lon': self.obj.location.lon}}
        response = client.get('/object/2', headers=self.headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An object with this id was not found'}


    def test_edit_object(self):
        pass


    def test_delete_object(self):
        response = client.delete('/object/1', headers=self.headers)
        assert response.status_code == 200
        assert response.json() == {"id": 1,
                                   "name": self.obj.name,
                                   "description": self.obj.description,
                                   "location": {'lat': self.obj.location.lat, 'lon': self.obj.location.lon}}
        response = client.delete('/object/1', headers=self.headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An object with this id was not found'}
