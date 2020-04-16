from celery import Celery

from config import ConfigCelery

celery = Celery('celery_app')
celery.config_from_object(ConfigCelery)
