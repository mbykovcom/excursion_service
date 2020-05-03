import unittest
from datetime import datetime, timedelta

import mock

import celery_app
from database import db
from database.connection import Database
from models.user import User
from controllers import user as user_service
from models.user_excurion import UserExcursion
from utils.auth import get_hash_password


class TestCelery:

    def setup_class(cls):
        pass

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        user_excursions = db.get_collection('user_excursions')
        keys = db.get_collection('table_keys')
        users.delete_many({})
        user_excursions.delete_many({})
        keys.delete_many({})

    @mock.patch("celery_app.send_email", mock.MagicMock(return_value=True))
    def test_send_email(self):
        result = celery_app.send_email('bykov@appvelox.ru', 'Test', 'Test')
        assert result is True

    @mock.patch("celery_app.clearing_inactive_users", mock.MagicMock(return_value=True))
    def test_clearing_inactive_users(self):
        user = User('user_1@email.ru', get_hash_password('Password_1'), 'User')
        user.date_registration = datetime.now() - timedelta(hours=25)
        user_service.create_user(user)
        assert celery_app.clearing_inactive_users() is True

    @mock.patch("celery_app.clearing_inactive_users", mock.MagicMock(return_value=True))
    def test_deactivate_user_excursions(self):
        user_excursions = [UserExcursion(1, 1, True, date_added=datetime.now() - timedelta(days=31)),
                           UserExcursion(2, 2, True, date_added=datetime.now() - timedelta(days=30))]
        db.add(user_excursions[0])
        db.add(user_excursions[1])
        assert celery_app.deactivate_user_excursions() is True


if __name__ == '__main__':
    unittest.main()
