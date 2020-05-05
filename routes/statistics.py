from datetime import datetime, timedelta

from fastapi import APIRouter, Header, Body
from starlette import status

from models.other import Statistics

from controllers import statistics as statistics_service
from utils import auth

router = APIRouter()


@router.get('/user', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_users(jwt: str = Header(..., example='key'),
                               start: datetime = Body(None, example={'start': datetime.now() - timedelta(days=2)}),
                               end: datetime = Body(None, example={'end': datetime.now()})):
    auth.authentication(jwt, 'admin')
    if type(start) is str:
        start = datetime.fromisoformat(start)
    if type(end) is str:
        end = datetime.fromisoformat(end)

    period = statistics_service.specify_period(start, end)
    statistics = statistics_service.get_statistics_users(period)
    return statistics


@router.get('/excursion', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_excursions(jwt: str = Header(..., example='key'),
                               start: datetime = Body(None, example={'start': datetime.now() - timedelta(days=2)}),
                               end: datetime = Body(None, example={'end': datetime.now()})):
    auth.authentication(jwt, 'admin')
    if type(start) is str:
        start = datetime.fromisoformat(start)
    if type(end) is str:
        end = datetime.fromisoformat(end)

    period = statistics_service.specify_period(start, end)
    statistics = statistics_service.get_statistics_excursions(period)
    return statistics


@router.get('/listening', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_listening(jwt: str = Header(..., example='key'),
                               start: datetime = Body(None, example={'start': datetime.now() - timedelta(days=2)}),
                               end: datetime = Body(None, example={'end': datetime.now()})):
    auth.authentication(jwt, 'admin')
    if type(start) is str:
        start = datetime.fromisoformat(start)
    if type(end) is str:
        end = datetime.fromisoformat(end)

    period = statistics_service.specify_period(start, end)
    statistics = statistics_service.get_statistics_listening(period)
    return statistics


@router.get('/sales', status_code=status.HTTP_200_OK, response_model=Statistics)
async def get_statistics_sales(jwt: str = Header(..., example='key'),
                               start: datetime = Body(None, example={'start': datetime.now() - timedelta(days=2)}),
                               end: datetime = Body(None, example={'end': datetime.now()})):
    auth.authentication(jwt, 'admin')
    if type(start) is str:
        start = datetime.fromisoformat(start)
    if type(end) is str:
        end = datetime.fromisoformat(end)

    period = statistics_service.specify_period(start, end)
    statistics = statistics_service.get_statistics_sales(period)
    return statistics
