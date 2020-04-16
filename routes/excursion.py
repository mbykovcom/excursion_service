from typing import List

from fastapi import status, Body, HTTPException, APIRouter, Header

from models.buy import BuyOut
from models.excursion import ExcursionOut, ExcursionIn, ExcursionDetails
from models.other import Error

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ExcursionOut, responses={401: {'model': Error}})
async def create_excursion(excursion: ExcursionIn = Body(..., example={"id_route": 1,
                                                                       "name": "Excursion name",
                                                                       "description": "Excursion description",
                                                                       "price": 100.00}),
                           jwt: str = Header(..., example='key')):
    pass


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ExcursionOut], responses={401: {'model': Error}})
async def get_excursions(jwt: str = Header(..., example='key')):
    pass


@router.post("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=BuyOut,
             responses={400: {'model': Error}, 401: {'model': Error}})
async def buy_excursion(excursion_id: int, jwt: str = Header(..., example='key')):
    pass


@router.get("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionDetails,
            responses={400: {'model': Error}, 401: {'model': Error}})
async def get_excursion_by_id(excursion_id: int, jwt: str = Header(..., example='key')):
    pass


@router.put("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionOut,
            responses={400: {'model': Error}, 401: {'model': Error}})
async def edit_excursion(excursion_id: int, excursion: ExcursionIn = Body(..., example={"id_route": 1,
                                                                                        "name": "New name",
                                                                                        "description": "New description",
                                                                                        "price": 120.00}),
                         jwt: str = Header(..., example='key')):
    pass


@router.delete("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionOut,
               responses={400: {'model': Error}, 401: {'model': Error}})
async def delete_excursion_by_id(excursion_id: int, jwt: str = Header(..., example='key')):
    pass
