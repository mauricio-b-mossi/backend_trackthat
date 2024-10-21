from typing import Annotated
from sqlmodel import select, col
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from ..dependencies import SessionDep
from passlib.context import CryptContext 
from app.models import User, UserBase
from datetime import timedelta, timezone, datetime
import jwt


# EXTRACT THIS TO ENV.
SECRET_KEY = "0bff56c7b85f5df372caaddbded53979155d91485f4d2762469a28234c535e69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

class UserInSignUp(BaseModel):
    name : str
    email : EmailStr
    password : str

class UserInLogin(BaseModel):
    name : str | None
    email : EmailStr | None
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str


auth_scheme = OAuth2PasswordBearer("auth/login")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(plain_password : str, hash_password : str):
     return pwd_context.verify(plain_password, hash_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta # expires in time delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15) # expires in 15 mins by default
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/signup")
async def signup(user : Annotated[UserInSignUp, Body()], session : SessionDep) -> UserBase:
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
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session : SessionDep
) -> Token:
    user = session.exec(select(User).where(col(User.name) == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
            data={"sub": f"{user.id}:{user.name}"}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer") 
