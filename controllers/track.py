"""
Module for working with track
"""

from typing import List

from fastapi import HTTPException
from starlette import status

import boto3

from database import db
from models.track import Track

from config import Config

URL = f'{Config.S3_END_POINT}/{Config.BUCKET}'


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
            response = client_s3.delete_object(Bucket=Config.BUCKET, Key=f'{track.name}.mp3')
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


def update_track(track_id: int, track_binary: bytes = None, name: str = None) -> Track:
    """
    Updates an track in the collection
    :param track_id: Track id to update
    :param track_binary: update the data track
    :param name: update the name of the track
    :return: updated track
    """
    if track_binary is None and name is None:
        return None
    track = get_track_by_id(track_id)
    if not track:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='A track with this id was not found')
    if name is not None and track_binary is not None:
        if delete_track_form_cloud(track.name):
            if not add_track_in_cloud(track_binary, name):
                return None
        else:
            return None
        track.name = name
        track.url = f'{URL}/{track.name}.mp3'
    else:
        if name is not None:
            track_binary = get_track_from_cloud(track.name)
            if delete_track_form_cloud(track.name):
                if not add_track_in_cloud(track_binary, name):
                    return None
                track.name = name
                track.url = f'{URL}/{track.name}.mp3'
            else:
                return None
        else:
            if delete_track_form_cloud(track.name):
                if not add_track_in_cloud(track_binary, track.name):
                    return None
            else:
                return None
            return track
    if db.update_item(track):
        return track
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Failed to update the track')


def get_tracks_by_list_id(list_id: List[int]) -> List[Track]:
    """
    Get an list track from the collection by list id
    :param list_id: list id of the track you are looking for
    :return: desired list track
    """
    list = db.get_items_by_list_id('tracks', list_id)
    return list


# S3 functions


def create_client_s3():
    """
    Create a client for working with DigitalOcean storage
    :return: client DigitalOcean storage
    """
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=Config.REGION,
                            endpoint_url=Config.S3_END_POINT,
                            aws_access_key_id=Config.S3_ACCESS_KEY,
                            aws_secret_access_key=Config.S3_SECRET_ACCESS_KEY)
    return client


def add_track_in_cloud(track_data: bytes, name: str):
    """
    Upload a file to DigitalOcean storage
    :param track_data: file in binary format
    :param name: File name
    :return: result True | False
    """
    client_s3 = create_client_s3()
    result = client_s3.put_object(Bucket=Config.BUCKET, Key=f'{name}.mp3', Body=track_data)
    if result['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def get_track_from_cloud(name: str) -> bytes:
    """
    Get a file from the DigitalOcean storage by file name
    :param name: File name
    :return: file in binary format
    """
    client_s3 = create_client_s3()
    result = client_s3.get_object(Bucket=Config.BUCKET, Key=f'{name}.mp3')
    return result['Body'].read()


def delete_track_form_cloud(name: str):
    """
    Delete a file from the DigitalOcean storage by file name
    :param name: File name
    :return: result True | False
    """
    client_s3 = create_client_s3()
    result = client_s3.delete_object(Bucket=Config.BUCKET, Key=name)
    if result['ResponseMetadata']['HTTPStatusCode'] == 204:  # Boto3 bug: always returns 204
        return True
    else:
        return False
