import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # App
    SECRET_KEY = os.environ.get('SECRET_KEY', 'test-excursion-service')
    # DataBase
    URL_MONGODB = os.environ.get('URL_MONGODB', 'mongodb://localhost:27017/')
    DATABASE = os.environ.get('DATABASE', 'excursion-service')
    # Email settings
    SMTP_SERVER = os.environ.get('SMPT_SERVER', 'smtp.yandex.ru')
    SMTP_PORT = os.environ.get('SMTP_PORT', 587)
    EMAIL = os.environ.get('EMAIL', 'bykov@appvelox.ru')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', '9Fhc7RnZ1kMV')
    # Token settings
    ALGORITHM = os.environ.get('ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    # Celery Parameters
    REGISTRATION_EXPIRE_HOURS = os.environ.get('REGISTRATION_EXPIRE_HOURS', 24)
    # Administration settings
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@realty.ru')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin')
    URL_SERVICE = os.environ.get('URL_SERVICE', 'http://0.0.0.0')
    # Cloud storage S3
    S3_END_POINT = os.environ.get('S3_END_POINT', 'https://excursion.fra1.digitaloceanspaces.com')
    REGION = os.environ.get('REGION', 'fra1')
    S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', 'V5L5K6H7M4H6B5GUD34A')
    S3_SECRET_ACCESS_KEY = os.environ.get('S3_SECRET_ACCESS_KEY', 'E0IfzUunahTvdQYx1epEE9wSf0Al0wKYhqfOLOHOoXU')
    BUCKET = os.environ.get('BUCKET', 'Track')
    # Yandex static maps
    MAP = os.environ.get('MAP', 'https://static-maps.yandex.ru/1.x/?')
    TYPE_MAP = os.environ.get('TYPE_MAP', 'map')
    ZOOM_MAP = os.environ.get('ZOOM_MAP', '13')

class ConfigCelery:
    broker_url = os.environ.get('BROKER_URL', 'redis://localhost:6379')
    result_backend = os.environ.get('RESULT_BACKEND', 'redis://localhost:6379')
    task_serializer = os.environ.get('TASK_SERIALIZER', 'json')
    result_serializer = os.environ.get('RESULT_SERIALIZER', 'json')
    accept_content = os.environ.get('ACCEPT_CONTENT', ['json'])
    timezone = os.environ.get('TIMEZONE', 'Europe/Moscow')
    enable_utc = os.environ.get('ENABLE_UTC', 'Europe/Moscow')
