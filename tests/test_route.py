from datetime import timedelta
from time import sleep

from starlette.testclient import TestClient

from app import app
from config import Config
from database.connection import Database
from models.user import User
from utils import auth
from utils.auth import get_hash_password

client = TestClient(app)


class TestAuth:

    def setup_class(cls):
        cls.user = User('user@email.ru', get_hash_password('Password_1'), 'User')
        cls.jwt = None

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
                                                expires_delta=timedelta(hours=Config.REGISTRATION_EXPIRE_HOURS)).decode()

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
                                                expires_delta=timedelta(hours=Config.REGISTRATION_EXPIRE_HOURS)).decode()
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
