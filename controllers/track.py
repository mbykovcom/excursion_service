from typing import List

from fastapi import HTTPException, UploadFile
from starlette import status

import boto3

from database import db
from models.track import Track, TrackUpdate

from config import Config

URL = f'https://{Config.S3_END_POINT}/{Config.BUCKET}'


def add_track(track_data: bytes, name: str) -> Track:
    """
    Add a new track to the collection
    :param track_data: track data
    :param name: track name
    :return: track added to the collection
    """
    if db.get_track_by_name(name):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail='A track with this name already exists')
    if add_track_in_cloud(track_data, name):
        track_id = db.get_last_id('tracks').last_id
        track = db.add(Track(name, f'{URL}/{name}.mp3', track_id))
        track.track = track_data
        return track
    return None


def delete_track(id: int) -> Track:
    """
    Delete an track from the collection
    :param id: id of the object to delete
    :return: object deleted from the collection
    """
    track = db.get_data_by_id(id, 'tracks')
    if track:
        if db.delete(id, 'tracks'):
            client_s3 = create_client_s3()
            response = client_s3.delete_object(Bucket=Config.BUCKET, Key=track.name)
            return track
    return None


def get_tracks() -> List[Track]:
    """
    Get all tracks from the collection
    :return: list of tracks
    """
    tracks = db.get_all_items('tracks')
    return tracks


def get_track_by_id(id: int) -> Track:
    """
    Get an track from the collection by id
    :param id: id of the track you are looking for
    :return: desired track
    """
    return db.get_data_by_id(id, 'tracks')


def update_object(track_id: int, track_update: TrackUpdate) -> Track:
    """
       Updates an track in the collection
       :param track_id: Track id to update
       :param track_update: update the data track
       :return: updated track
       """
    track = get_track_by_id(track_id)
    if not track:
        return None
    if track_update.name is not None and track_update.track is not None:
        if delete_track_form_cloud(track.name):
            if not add_track_in_cloud(track_update.track, track_update.name):
                return None
        else:
            return None
    flag_update_track = False
    if track_update.name is not None:
        if delete_track_form_cloud(track.name):
            if track_update.track is not None:
                if add_track_in_cloud(track_update.track, track.name):
                    track.name = track_update.name
                    track.url = f'{URL}/{track.name}.mp3'
                    flag_update_track = True
                return None
            else:
                client = create_client_s3()
        else:
            return None
    if track_update.track is not None:
        track.track = track_update.track

    if db.update_item(track):
        return track
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the object')


# S3 functions


def create_client_s3():
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=Config.REGION,
                            endpoint_url=Config.S3_END_POINT,
                            aws_access_key_id=Config.S3_ACCESS_KEY,
                            aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY)
    return client


def add_track_in_cloud(track_data: bytes, name: str):
    client_s3 = create_client_s3()
    result = client_s3.put_object(Bucket=Config.BUCKET, Key=name, Body=track_data)
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def delete_track_form_cloud(name: str):
    client_s3 = create_client_s3()
    result = client_s3.delete_object(Bucket=Config.BUCKET, Key=name)
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False
