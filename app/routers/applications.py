from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Annotated


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    responses={404: {"description": "Not found"}}
)

fake_app_db = []

@router.get("/")
async def get_all_apps(skip : Annotated[int, Query()] = 0, limit : Annotated[int, Query()] = 20, return_all : Annotated[bool, Query()] = False, sort : Annotated[bool, Query()] = False):
    if return_all:
        return fake_app_db
    
    if sort:
        sorted_apps = fake_app_db
        sorted_apps.sort(key = lambda Application : Application.date)
        return sorted_apps
    
    return fake_app_db[skip : skip + limit]


@router.get("/{application_id}")
async def get_application(application_id : int):
    return fake_app_db[application_id]

