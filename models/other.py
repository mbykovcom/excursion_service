from pydantic import BaseModel, Field, EmailStr


class TableKey:
    def __init__(self, _id: int, table: str, last_id: int):
        self._id: int = _id
        self.table: str = table
        self.last_id: int = last_id


class Auth(BaseModel):
    email: EmailStr = Field(..., description='The email a user')
    password: str = Field(..., description='The password a user', min_length=4)


class Token(BaseModel):
    access_token: str = Field(..., description='Access token')
    token_type: str = Field(..., description='Token type')


class Statistics(BaseModel):
    type: str = Field(..., description='Type statistics')
    data: dict = Field(..., description='A dictionary, where the key is the x value, and the value is the y value')


class Error(BaseModel):
    code: int = Field(..., description="Error code")
    detail: str = Field(..., description='Error details')
