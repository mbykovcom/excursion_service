from fastapi import APIRouter, Body
from starlette import status

from models.other import Error, Token
from models.user import UserOut, UserIn

router = APIRouter()


@router.post("/registration", status_code=status.HTTP_201_CREATED, response_model=UserOut,
             responses={400: {'model': Error}})
async def registration(user_data: UserIn = Body(..., example={"email": "name@email.ru",
                                                              "password": "password",
                                                              "name": "Nick"})):
    pass


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
async def login(user_data: UserIn = Body(..., example={"email": "name@email.ru",
                                                       "password": "password"})):
    pass
