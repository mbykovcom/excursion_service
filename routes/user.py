from typing import List

from fastapi import APIRouter, Header
from starlette import status

from models.user_excurion import UserExcursionOut

router = APIRouter()


@router.get('/excursion', status_code=status.HTTP_200_OK, response_model=List[UserExcursionOut])
async def get_users_excursions(jwt: str = Header(..., example='key')):
    pass


@router.get('/excursion/{user_excursion_id}', status_code=status.HTTP_200_OK, response_model=UserExcursionOut)
async def get_users_excursion_by_id(user_excursion_id: int, jwt: str = Header(..., example='key')):
    pass
