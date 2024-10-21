from typing import Annotated
from sqlmodel import select, col
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel, EmailStr
from ..dependencies import SessionDep
from passlib.context import CryptContext 
from app.models import User, UserOut

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_passowrd(plain_password : str, hash_password : str):
    return pwd_context.verify(plain_password, hash_password)

def get_password_hash(password):
    return pwd_context.hash(password)


class UserInSignUp(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserInLogin(BaseModel):
    name : str | None
    email : EmailStr | None
    password : str


@router.post("/signup")
async def signup(user : Annotated[UserInSignUp, Body()], session : SessionDep) -> UserOut:
    user_find = session.exec(select(User).where(col(User.name) == user.name)).first()
    if user_find:
       raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists.",
            )
    newuser = User(name = user.name, email=user.email, password=get_password_hash(user.password))
    session.add(newuser)
    session.commit()
    session.refresh(newuser)
    return newuser

@router.post("/login")
async def login(user : Annotated[UserInLogin, Body()], session : SessionDep):
    pass
