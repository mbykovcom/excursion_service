from typing import List

from fastapi import APIRouter, Header, HTTPException
from starlette import status

from models.track import TrackOut
from models.user_excurion import UserExcursionsDetail, UserExcursionDetail

from controllers import user_excursion as user_excursion_service
from controllers import excursion_point as point_service
from controllers import track as track_service

from utils import auth

router = APIRouter()


@router.get('/excursion', status_code=status.HTTP_200_OK, response_model=List[UserExcursionDetail])
async def get_user_excursions(jwt: str = Header(..., example='key')):
    user = auth.authentication(jwt)
    user_excursions = user_excursion_service.get_user_excursions_by_user_id(user._id)
    list_user_excursion = list(map(user_excursion_service.user_excursions_detail, user_excursions))
    return list_user_excursion


@router.get('/excursion/{user_excursion_id}', status_code=status.HTTP_200_OK,
            response_model=UserExcursionsDetail)
async def get_user_excursion_by_id(user_excursion_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt)
    user_excursion = user_excursion_service.get_user_excursion_by_id(user_excursion_id)
    if not user_excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='An user excursion with this id was not found')
    details_excursion = user_excursion_service.user_excursion_detail(user_excursion)
    return details_excursion


@router.get('/excursion/{user_excursion_id}/play', status_code=status.HTTP_200_OK, response_model=TrackOut)
async def get_last_track_user_excursion(user_excursion_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt)
    user_excursion = user_excursion_service.get_user_excursion_by_id(user_excursion_id)
    if not user_excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='An user excursion with this id was not found')
    if user_excursion.id_last_point == 0:
        last_excursion_point = point_service.get_excursion_points_by_excursion(user_excursion.id_excursion)[0]
    else:
        last_excursion_point = point_service.get_excursion_point_by_id(user_excursion.id_last_point)
    track = track_service.get_track_by_id(last_excursion_point.id_track).track_out()
    return track


@router.get('/excursion/{user_excursion_id}/play/{track_id}', status_code=status.HTTP_200_OK, response_model=TrackOut)
async def get_track_user_excursion_by_id(user_excursion_id: int, track_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt)
    user_excursion = user_excursion_service.get_user_excursion_by_id(user_excursion_id)
    if not user_excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='An user excursion with this id was not found')

    if not point_service.check_track_in_excursion(user_excursion.id_excursion, track_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The track with this id was not found')
    track = track_service.get_track_by_id(track_id)
    user_excursion.id_last_point = track_id
    user_excursion_service.update_last_point(user_excursion)
    return track.track_out()
