import unittest
from datetime import datetime, timedelta

import mock

import celery_app
from database.connection import Database
from models.user import User
from controllers import user as user_service
from utils.auth import get_hash_password


class TestCelery:

    def setup_class(cls):
        pass

    def teardown_class(cls):
        db = Database()
        users = db.get_collection('users')
        keys = db.get_collection('table_keys')
        users.delete_many({})
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


if __name__ == '__main__':
    unittest.main()
