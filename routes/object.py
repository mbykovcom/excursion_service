from typing import List

from fastapi import status, Body, HTTPException, APIRouter, Header

from models.object import ObjectOut, ObjectIn, Object, ObjectUpdate
from models.other import Error
from controllers import object as obj
from utils import auth

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ObjectOut,
             responses={401: {'model': Error},
                        500: {'model': Error}})
async def create_object(obj_data: ObjectIn = Body(..., example={"name": "Name of the point",
                                                                "description": "Description",
                                                                "location": {'lat': 59.93904113769531,
                                                                             'lon': 30.3157901763916}}),
                        jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    new_obj = Object(**obj_data.dict())
    new_obj = obj.create_object(new_obj)
    if new_obj:
        return new_obj.object_out()
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error creating an object')


@router.get("", status_code=status.HTTP_200_OK, response_model=List[ObjectOut], responses={401: {'model': Error}})
async def get_objects(jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    objects = obj.get_objects()
    return [object_.object_out() for object_ in objects]


@router.get("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
            responses={401: {'model': Error}, 404: {'model': Error}})
async def get_object_by_id(object_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    object_ = obj.get_object_by_id(object_id)
    if not object_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An object with this id was not found')
    return object_.object_out()


@router.put("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
            responses={401: {'model': Error}, 404: {'model': Error}})
async def edit_object(object_id: int, obj_update: ObjectUpdate = Body(..., example={"name": "New name of the point",
                                                                                    "description": "New description",
                                                                                    "location": {
                                                                                        'lat': 59.93904113769531,
                                                                                        'lon': 30.3157901763916}}),
                      jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    update_object = obj.update_object(object_id, obj_update)
    if update_object:
        return update_object.object_out()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An object with this id was not found')


@router.delete("/{object_id}", status_code=status.HTTP_200_OK, response_model=ObjectOut,
               responses={401: {'model': Error}, 404: {'model': Error}})
async def delete_object_by_id(object_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    object_ = obj.delete_object(object_id)
    if not object_:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='An object with this id was not found')
    return object_.object_out()
