import re
from datetime import timedelta, datetime

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from passlib.context import CryptContext
from starlette import status

from config import Config
from database import db
from models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_strength_point(match) -> int:
    return 1 if match else 0


def checking_password_complexity(password: str) -> str:
    strength_point = 0
    strength_point += get_strength_point(len(password) > 8)
    strength_point += get_strength_point(re.search(r"\d", password))
    strength_point += get_strength_point(re.search(r"[A-Z]", password))
    strength_point += get_strength_point(re.search(r"[a-z]", password))
    strength_point += get_strength_point(re.search(r"\W", password))

    if 0 <= strength_point < 2:
        return 'Easy'
    elif 2 <= strength_point < 4:
        return 'Medium'
    else:
        return 'Hard'


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password):
    return pwd_context.hash(password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


def authentication(token: str = Depends(oauth2_scheme), role: str = 'user') -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    access_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access rights")
    registration_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No access rights,"
                                                                                         "please confirm registration.")

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = db.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    elif user.is_active is False:
        raise registration_exception
    elif user.role == 'user' != role:
        raise access_exception
    return user


def get_user_data(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except PyJWTError as e:
        print(f"Error: {e}")
        return None
    db_user = db.get_user_by_email(email)
    if db_user is None:
        return None
    return db_user
