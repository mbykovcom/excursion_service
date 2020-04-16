from typing import List

from fastapi import status, Body, HTTPException, APIRouter, Header

from models.object import ObjectOut, ObjectIn
from models.other import Error

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ObjectOut, responses={401: {'model': Error}})
async def create_object(object: ObjectIn = Body(..., example={"name": "Name of the point",
                                                              "location": {'lat': 59.93904113769531,
                                                                           'lon': 30.3157901763916},
                                                              "date_receipt": "2020-03-29 14:10:00"}),
                        jwt: str = Header(..., example='key')):
    pass


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ObjectOut], responses={401: {'model': Error}})
async def get_objects(jwt: str = Header(..., example='key')):
    pass


@router.get("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
            responses={400: {'model': Error}, 401: {'model': Error}})
async def get_object_by_id(object_id: int, jwt: str = Header(..., example='key')):
    pass


@router.put("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
            responses={400: {'model': Error}, 401: {'model': Error}})
async def edit_object(object_id: int, object: ObjectIn = Body(..., example={"name": "Name of the point",
                                                                            "location": {'lat': 59.93904113769531,
                                                                                         'lon': 30.3157901763916},
                                                                            "date_receipt": "2020-03-29 14:10:00"}),
                      jwt: str = Header(..., example='key')):
    pass


@router.delete("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
               responses={400: {'model': Error}, 401: {'model': Error}})
async def delete_object_by_id(object_id: int, jwt: str = Header(..., example='key')):
    pass