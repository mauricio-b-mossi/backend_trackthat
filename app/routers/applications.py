from fastapi import APIRouter, Depends, HTTPException, Query, Body, Path, status
from typing import Annotated
from sqlmodel import col, desc, select
from app.dependencies import SessionDep, get_current_user_id # Interface to database
from app.models import Application, User, ApplicationIn, ApplicationUpdate


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", status_code=status.HTTP_200_OK) # get_all was redundant in the presence of skip and limit. 
async def get_all_apps(
    session : SessionDep,
    user_id : Annotated[int, Depends(get_current_user_id)],
    sort : Annotated[bool, Query()] = False,
    skip : Annotated[int, Query()] = 0, 
    limit : Annotated[int, Query()] = 20, 
):
    if sort:
        return session.exec(select(Application).where(col(Application.user_id) == user_id).offset(skip).limit(limit).order_by(desc(Application.date))).all()
    return session.exec(select(Application).where(col(Application.user_id) == user_id).offset(skip).limit(limit)).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_application(session : SessionDep, user_id : Annotated[int, Depends(get_current_user_id)], application : Annotated[ApplicationIn, Body()]) -> Application:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User provided does not exist.")
    app = Application(**application.model_dump())
    user.applications.append(app)
    session.add(user)
    session.commit()
    session.refresh(app)
    return app


@router.get("/{application_id}", status_code=status.HTTP_200_OK)
async def get_application(session : SessionDep, user_id : Annotated[int, Depends(get_current_user_id)], application_id : Annotated[int, Path()]):
    app = session.exec(select(Application).where(col(Application.id) == application_id)).first()
    if app is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application with {application_id} does not exist.")
    if app.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return app

@router.patch("/{application_id}", status_code=status.HTTP_201_CREATED)
async def edit_application(session : SessionDep, user_id : Annotated[int, Depends(get_current_user_id)], application_id : Annotated[int, Path()], updated_application : Annotated[ApplicationUpdate, Body()]):
    app = session.exec(select(Application).where(col(Application.id) == application_id)).first()
    if app is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Application with {application_id} does not exist.")
    if app.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    app.sqlmodel_update(updated_application.model_dump(exclude_unset=True)) 
    session.add(app)
    session.commit()
    session.refresh(app)
    return app
