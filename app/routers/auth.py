from typing import Annotated
from sqlmodel import select, col
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Body, HTTPException, status, Depends
from pydantic import BaseModel, EmailStr
from ..dependencies import SessionDep
from passlib.context import CryptContext 
from app.models import User, UserOut
from datetime import timedelta, timezone, datetime
import jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="login")

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
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session : SessionDep
) -> Token:
    user = session.exec(select(User).where(col(User.name) == form_data.username)).one()
    if not verify_password(form_data.username, user.password):
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
