from datetime import timedelta

import jwt
from fastapi import APIRouter, Body, HTTPException
from jwt import PyJWTError
from starlette import status

from config import Config
from models.other import Error, Token
from models.user import UserOut, UserIn, User, UserAuth
from controllers import user as user_service
from utils import auth
from celery_app import send_email

router = APIRouter()


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserOut,
             responses={500: {'model': Error}})
async def registration(user_data: UserIn = Body(..., example={"email": "name@email.ru",
                                                              "password": "password",
                                                              "name": "Nick"})):
    if auth.checking_password_complexity(password=user_data.password) == 'Easy':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Your password is too simple. The password '
                                                                            'must contain uppercase and lowercase '
                                                                            'letters, as well as numbers and special '
                                                                            'characters')
    hash_password = auth.get_hash_password(user_data.password)
    db_user = User(email=user_data.email, hash_password=hash_password, name=user_data.name)
    if user_service.insert_db(db_user):
        access_token_expires = timedelta(hours=Config.REGISTRATION_EXPIRE_HOURS)
        access_token = auth.create_access_token(data={"sub": user_data.email}, expires_delta=access_token_expires)
        url = f'{Config.URL_SERVICE}/registration/{access_token}'
        send_email(user_data.email, title='Activate your account',
                   description=f'Click the link: {url} to activate your account. The link is valid for 24 hours')
        return UserOut(id=db_user._id, email=db_user.email, name=db_user.name, role=db_user.role,
                       date_registration=db_user.date_registration)
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Registration error')


@router.post("/registration/{token}", status_code=status.HTTP_200_OK, responses={400: {'model': Error},
                                                                                 404: {'model': Error},
                                                                                 500: {'model': Error}})
async def confirmation_registration(token: str):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid url')
    user = user_service.get_user_by_email(email)
    if user and user.is_active is False:
        result = user_service.activate_user(email)
        if result:
            send_email(email, title='Registering with excursion-service',
                       description=f'The user {email} was created successfully.')
            raise HTTPException(status_code=status.HTTP_200_OK, detail='The user activated')
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Activation error')
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid token')


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_data: UserAuth = Body(..., example={"email": "name@email.ru",
                                                         "password": "password"})):
    token = user_service.login(user_data)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials',
                            headers={"WWW-Authenticate": "Bearer"}, )
    return token
