import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery
from celery.schedules import crontab

from config import ConfigCelery, Config
from controllers import user as user_service
from database import db

celery = Celery('celery_app')
celery.config_from_object(ConfigCelery)

celery.conf.beat_schedule = {
    "inactive_users": {
        "task": 'celery_app.clearing_inactive_users',
        'schedule': crontab(hour=Config.REGISTRATION_EXPIRE_HOURS - 1, minute=59)
    },
    "deactivate_user_excursions": {
        "task": 'celery_app.deactivate_user_excursions',
        'schedule': crontab(hour=23, minute=59)
    }
}


@celery.task
def send_email(email, title, description) -> bool:
    """Send an email

    :param email: recipient's email address as name@email.com
    :param title: message subject
    :param description: the text of the letter
    :return: True if the email is sent, otherwise False
    """
    try:
        smtpObj = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
        smtpObj.starttls()
        smtpObj.login(Config.EMAIL, Config.EMAIL_PASSWORD)
        message = MIMEMultipart("alternative")
        message["Subject"] = title
        message["From"] = Config.EMAIL
        message["To"] = email
        msg = f"""\
                {description}"""
        message.attach(MIMEText(msg, 'plain'))
        smtpObj.sendmail(Config.EMAIL, email, message.as_string())
    except Exception as error:  # If an exception is raised when send email
        print(error)
        return False
    return True


@celery.task
def clearing_inactive_users() -> bool:
    """
    Clears the database from unverified users within a day
    :return: result
    """
    users = user_service.get_users_inactive_24_hours()
    return user_service.delete_users([user._id for user in users])


@celery.task
def deactivate_user_excursions() -> bool:
    """
    Deactivating a user's tour after 30 days of purchase
    :return: result True | False
    """
    expired_user_excursions = db.get_expired_user_excursions(Config.USER_EXCURSION_EXPIRE_DAYS)
    count = 0
    for user_excursion in expired_user_excursions:
        if db.deactivating_user_excursion(user_excursion._id):
            count += 1
    if count == len(expired_user_excursions):
        return True
    else:
        return False
