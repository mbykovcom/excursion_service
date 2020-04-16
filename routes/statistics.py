from datetime import datetime

from fastapi import APIRouter, Header
from starlette import status

from models.other import Statistics

router = APIRouter()


@router.get('/user', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_users(jwt: str = Header(..., example='key'), start: datetime = None, end: datetime = None):
    pass


@router.get('/excursion', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_excursions(jwt: str = Header(..., example='key'), start: datetime = None,
                                    end: datetime = None):
    pass


@router.get('/listening', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_listening(jwt: str = Header(..., example='key'), start: datetime = None, end: datetime = None):
    pass


@router.get('/sales', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_sales(jwt: str = Header(..., example='key'), start: datetime = None, end: datetime = None):
    pass
