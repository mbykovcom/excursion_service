from datetime import timedelta
from time import sleep

from starlette.testclient import TestClient

from app import app
from config import Config
from controllers.user import login, create_user
from database.connection import Database
from models.excursion import Excursion
from models.object import Object, Coordinates
from models.user import User, UserAuth
from utils import auth
from utils.auth import get_hash_password
from controllers import excursion as excursion_service

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
        json = {'name': 'Name update'}
        self.obj.name = json['name']
        response = client.put('/object/1', headers=self.headers, json=json)
        assert response.status_code == 200
        assert response.json() == {"id": 1,
                                   "name": json['name'],
                                   "description": self.obj.description,
                                   "location": {'lat': self.obj.location.lat, 'lon': self.obj.location.lon}}
        json['description'] = 'Update description'
        json['location'] = {'lat': 0.0, 'lon': 0.0}
        self.obj.description = json['description']
        self.obj.location = Coordinates(lat=json['location']['lat'], lon=json['location']['lon'])
        response = client.put('/object/1', headers=self.headers, json=json)
        assert response.status_code == 200
        assert response.json() == {"id": 1,
                                   "name": json['name'],
                                   "description": json['description'],
                                   "location": json['location']}
        response = client.get('/object/2', headers=self.headers, json=json)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An object with this id was not found'}

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


class TestExcursion:

    def setup_class(cls):
        cls.admin = User(email='admin@email.ru', hash_password=get_hash_password('AdminPassword_1'), name='Admin',
                         role='admin',
                         is_active=True)
        create_user(cls.admin)
        cls.user = User(email='user@email.ru', hash_password=get_hash_password('UserPassword_1'), name='User',
                        is_active=True)
        create_user(cls.user)

        cls.jwt = {'admin': login(UserAuth(email=cls.admin.email, password='AdminPassword_1')).access_token,
                   'user': login(UserAuth(email=cls.user.email, password='UserPassword_1')).access_token}

        cls.excursions = [Excursion(name='Excursion', description='Excursion`s description', price=100.5)]

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        excursions = db.get_collection('excursions')
        user_excursions = db.get_collection('user_excursions')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        excursions.delete_many({})
        user_excursions.delete_many({})
        keys.delete_many({})

    def test_create_excursion(self):
        json = {'name': self.excursions[0].name, 'description': self.excursions[0].description,
                'price': self.excursions[0].price}
        headers = {'jwt': self.jwt['admin']}
        response = client.post('/excursion', headers=headers, json=json)
        assert response.status_code == 201
        response = response.json()
        assert response == {'id': 1,
                            'name': self.excursions[0].name,
                            'description': self.excursions[0].description,
                            'price': self.excursions[0].price,
                            'url_map_route': None}
        self.excursions[0]._id = response['id']

    def test_get_excursion_by_id(self):
        self.excursions.append(Excursion(name='Excursion 2', description='Description 2', price=500.5,
                                         url_map_route='URL'))
        self.excursions[1]._id = excursion_service.create_excursion(self.excursions[1])._id
        headers = {'jwt': self.jwt['admin']}
        response = client.get("/excursion", headers=headers)
        response = client.get(f"/excursion/{self.excursions[0]._id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {'id': self.excursions[0]._id,
                                   'name': self.excursions[0].name,
                                   'description': self.excursions[0].description,
                                   'price': self.excursions[0].price,
                                   'url_map_route': self.excursions[0].url_map_route}
        headers = {'jwt': self.jwt['user']}
        response = client.get(f"/excursion/{self.excursions[0]._id}", headers=headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An excursion with this id was not found'}
        response = client.get(f"/excursion/{self.excursions[1]._id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {'id': self.excursions[1]._id,
                                   'name': self.excursions[1].name,
                                   'description': self.excursions[1].description,
                                   'price': self.excursions[1].price,
                                   'url_map_route': self.excursions[1].url_map_route}

    def test_get_excursions(self):
        headers = {'jwt': self.jwt['admin']}
        response = client.get("/excursion", headers=headers)
        assert response.status_code == 200
        response = response.json()
        assert len(response) == 2
        assert response[0] == {'id': self.excursions[0]._id,
                               'name': self.excursions[0].name,
                               'description': self.excursions[0].description,
                               'price': self.excursions[0].price,
                               'url_map_route': self.excursions[0].url_map_route}
        headers = {'jwt': self.jwt['user']}
        response = client.get("/excursion", headers=headers)
        assert response.status_code == 200
        response = response.json()
        assert len(response) == 1
        assert response[0] == {'id': self.excursions[1]._id,
                               'name': self.excursions[1].name,
                               'description': self.excursions[1].description,
                               'price': self.excursions[1].price,
                               'url_map_route': self.excursions[1].url_map_route}

    def test_edit_excursion(self):
        json = {'name': 'Name update'}
        headers = {'jwt': self.jwt['admin']}
        print(self.excursions)
        self.excursions[1].name = json['name']
        response = client.put(f"/excursion/{self.excursions[1]._id}", headers=headers, json=json)
        assert response.status_code == 200
        assert response.json() == {'id': self.excursions[1]._id,
                                   'name': self.excursions[1].name,
                                   'description': self.excursions[1].description,
                                   'price': self.excursions[1].price,
                                   'url_map_route': self.excursions[1].url_map_route}
        json['description'] = 'Update description'
        json['price'] = 1010.99
        self.excursions[1].description = json['description']
        self.excursions[1].price = json['price']
        response = client.put(f"/excursion/{self.excursions[1]._id}", headers=headers, json=json)
        assert response.status_code == 200
        assert response.json() == {'id': self.excursions[1]._id,
                                   'name': self.excursions[1].name,
                                   'description': self.excursions[1].description,
                                   'price': self.excursions[1].price,
                                   'url_map_route': self.excursions[1].url_map_route}
        response = client.get('/excursion/10', headers=headers, json=json)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An excursion with this id was not found'}

    def test_buy_excursion(self):
        headers = {'jwt': self.jwt['user']}
        response = client.post(f"/excursion/{self.excursions[1]._id}", headers=headers)
        assert response.status_code == 200
        response = response.json()
        assert response['id_excursion'] == self.excursions[1]._id
        assert response['is_active'] is True
        response = client.post(f"/excursion/{self.excursions[0]._id}", headers=headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An excursion with this id was not found'}
        response = client.post(f"/excursion/10", headers=headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An excursion with this id was not found'}

    def test_delete_excursion(self):
        headers = {'jwt': self.jwt['admin']}
        response = client.delete(f"/excursion/{self.excursions[0]._id}", headers=headers)
        assert response.status_code == 200
        assert response.json() == {'id': self.excursions[0]._id,
                                   'name': self.excursions[0].name,
                                   'description': self.excursions[0].description,
                                   'price': self.excursions[0].price,
                                   'url_map_route': self.excursions[0].url_map_route}
        response = client.delete(f"/excursion/{self.excursions[0]._id}", headers=headers)
        assert response.status_code == 404
        assert response.json() == {'detail': 'An excursion with this id was not found'}
