from fastapi import Depends
from typing import Annotated
from sqlmodel import Session
from app.models import engine

def get_session():
    with Session(engine) as s:
        yield s

SessionDep = Annotated[Session, Depends(get_session)]
