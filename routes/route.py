# from typing import List
#
# from fastapi import status, Body, HTTPException, APIRouter, Header
#
# from models.other import Error
# from models.excursion_point import RouteIn, RouteOut, RouteDetails
#
# router = APIRouter()
#
#
# @router.post("", status_code=status.HTTP_201_CREATED, response_model=RouteOut, responses={401: {'model': Error}})
# async def create_route(route: RouteIn = Body(..., example={"name": "Route name",
#                                                            "route": [1, 2, 3]}),
#                        jwt: str = Header(..., example='key')):
#     pass
#
#
# @router.get("", status_code=status.HTTP_200_OK, response_model=List[RouteOut], responses={401: {'model': Error}})
# async def get_routes(jwt: str = Header(..., example='key')):
#     pass
#
#
# @router.get("/{route_id}", status_code=status.HTTP_200_OK, response_model=RouteDetails,
#             responses={400: {'model': Error}, 401: {'model': Error}})
# async def get_route_by_id(route_id: int, jwt: str = Header(..., example='key')):
#     pass
#
#
# @router.put("/{route_id}", status_code=status.HTTP_200_OK, response_model=RouteOut,
#             responses={400: {'model': Error}, 401: {'model': Error}})
# async def edit_route(route_id: int, route: RouteIn = Body(..., example={"name": "New name",
#                                                                         "route": [1, 3, 2]}),
#                      jwt: str = Header(..., example='key')):
#     pass
#
#
# @router.delete("/{route_id}", status_code=status.HTTP_200_OK, response_model=RouteOut,
#                responses={400: {'model': Error}, 401: {'model': Error}})
# async def delete_route_by_id(route_id: int, jwt: str = Header(..., example='key')):
#     pass
