from datetime import datetime, timedelta

from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description='The email a user')
    password: str = Field(..., description='The password a user', min_length=4) # TODO: Сделать проверку сложности пароля


class UserIn(UserAuth):
    name: str = Field(..., description='User name in service')


class UserOut(BaseModel):
    id: int = Field(..., description='User id')
    email: EmailStr = Field(..., description='The email a user')
    name: str = Field(..., description='User name in service')
    role: str = Field(..., description='The role a user in app')
    date_registration: datetime = Field(..., description='Date of user registration in the system')


class User:
    def __init__(self, email: str, hash_password: str, name: str, _id: int = None, role: str = 'user',
                 is_active: bool = False, date_registration: datetime = datetime.now()):
        self._id: int = _id
        self.email: str = email
        self.hash_password: str = hash_password
        self.name: str = name
        self.role: str = role
        self.is_active: bool = is_active
        self.date_registration = date_registration
