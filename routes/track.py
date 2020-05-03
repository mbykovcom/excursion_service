from typing import List

from fastapi import APIRouter, HTTPException, UploadFile, File, Header, Form
from starlette import status

from models.other import Error
from models.track import TrackOut
from controllers import track as track_service
from utils import auth

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TrackOut, responses={401: {'model': Error},
                                                                                          500: {'model': Error}})
async def add_track_storage(track_data: UploadFile = File(...), name: str = Form(...),
                            jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    file_extension = track_data.filename.split('.')[1]
    if file_extension not in ['mp3']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file extension')
    track_binary = track_data.file.read()
    track = track_service.add_track(track_binary, name)
    if not track:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='The track was not added, '
                                                                                      'an error occurred when adding '
                                                                                      'the track')
    return track.track_out()


@router.get("", status_code=status.HTTP_200_OK, response_model=List[TrackOut], responses={401: {'model': Error},
                                                                                          500: {'model': Error}})
async def get_tracks(jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    tracks = track_service.get_tracks()
    return [track.track_out() for track in tracks]


@router.get("/{track_id}", status_code=status.HTTP_200_OK, response_model=TrackOut, responses={401: {'model': Error},
                                                                                               404: {'model': Error},
                                                                                               500: {'model': Error}})
async def get_track_by_id(track_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    track = track_service.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='A track with this id was not found')
    return track.track_out()


@router.put("/{track_id}", status_code=status.HTTP_200_OK, response_model=TrackOut,
            responses={400: {'model': Error}, 401: {'model': Error}, 404: {'model': Error}, 500: {'model': Error}})
async def edit_track(track_id: int, track_data: UploadFile = File(None), name: str = Form(None),
                      jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')

    if track_data is None and name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request: no data was received for '
                                                                            'updating')

    track = track_service.get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='A track with this id was not found')
    if track_data is not None:
        file_extension = track_data.filename.split('.')[1]
        if file_extension not in ['mp3']:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file extension')

        track_binary = track_data.file.read()
    else:
        track_binary = None
    update_track = track_service.update_track(track_id, track_binary, name)
    if update_track:
        return update_track.track_out()
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='The track was not updated, '
                                                                                      'an error occurred when updating '
                                                                                      'the track')


@router.delete("/{track_id}", status_code=status.HTTP_200_OK, response_model=TrackOut,
               responses={401: {'model': Error}, 404: {'model': Error}})
async def delete_object_by_id(track_id: int, jwt: str = Header(..., example='key')):
    auth.authentication(jwt, 'admin')
    track = track_service.delete_track(track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='A track with this id was not found')
    return track.track_out()
