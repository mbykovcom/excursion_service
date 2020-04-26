from typing import List

from fastapi import status, Body, HTTPException, APIRouter, Header

from models.buy import Buy
from models.excursion import ExcursionOut, ExcursionIn, Excursion, ExcursionUpdate
from models.other import Error
from models.user_excurion import UserExcursionOut
from controllers import excursion as excursion_service
from utils import auth

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ExcursionOut, responses={401: {'model': Error}})
async def create_excursion(excursion_data: ExcursionIn = Body(..., example={"name": "Excursion name",
                                                                            "description": "Excursion description",
                                                                            "price": 100.00}),
                           jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    new_excursion = Excursion(**excursion_data.dict())
    excursion = excursion_service.create_excursion(new_excursion)
    return excursion.excursion_out()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ExcursionOut], responses={401: {'model': Error}})
async def get_excursions(jwt: str = Header(..., example='key')):
    user = auth.authentication(jwt)
    excursions = excursion_service.get_excursions(user.role)
    return [excursion.excursion_out() for excursion in excursions]


@router.post("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=UserExcursionOut,
             responses={401: {'model': Error}, 404: {'model': Error}})
async def buy_excursion(excursion_id: int, jwt: str = Header(..., example='key')):
    user = auth.authentication(jwt)
    bought_excursion = excursion_service.buy_excursion(excursion_id, user._id)
    if not bought_excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')
    return bought_excursion.user_excursion_out()


@router.get("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionOut,
            responses={401: {'model': Error}, 404: {'model': Error}})
async def get_excursion_by_id(excursion_id: int, jwt: str = Header(..., example='key')):
    user = auth.authentication(jwt)
    excursion = excursion_service.get_excursion_by_id(excursion_id)
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')
    if excursion.url_map_route is None and user.role == 'user':
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')
    return excursion.excursion_out()


@router.put("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionOut,
            responses={400: {'model': Error}, 401: {'model': Error}})
async def edit_excursion(excursion_id: int, excursion_update: ExcursionUpdate = Body(..., example={"id_route": 1,
                                                                                                   "name": "New name",
                                                                                                   "description": "New description",
                                                                                                   "price": 120.00}),
                         jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    update_excursion = excursion_service.update_excursion(excursion_id, excursion_update)
    if update_excursion:
        return update_excursion.excursion_out()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')


@router.delete("/{excursion_id}", status_code=status.HTTP_200_OK, response_model=ExcursionOut,
               responses={401: {'model': Error}, 404: {'model': Error}})
async def delete_excursion_by_id(excursion_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    excursion = excursion_service.delete_excursion(excursion_id)
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An excursion with this id was not found')
    return excursion.excursion_out()
