from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from todo_app.db import SessionLocal
from todo_app.responses import (
    LOGIN_RESPONSES,
    CREATE_USER_RESPONSES,
    FETCH_USER_RESPONSES,
)
from todo_app.config import settings
import todo_app.models as models
from todo_app.schemas import CreateUserSchema


SECRET_KEY = settings.secret_key
HASHING_ALGORITHM = settings.hashing_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(username: str):
    with SessionLocal() as session:
        user = (
            session.query(models.User).filter(models.User.username == username).first()
        )

    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/create/user", status_code=204, responses=CREATE_USER_RESPONSES)
async def create_new_user(create_user_schema: CreateUserSchema):
    """
    Create a new user
    """
    with SessionLocal() as session:
        username_exists = bool(
            session.query(models.User)
            .filter(models.User.username == create_user_schema.username)
            .first()
        )
        if username_exists:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
            )
        create_user_model = models.User()
        create_user_model.username = create_user_schema.username
        email_exists = bool(
            session.query(models.User)
            .filter(models.User.email == create_user_schema.email)
            .first()
        )
        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="An account with the specified email already exists",
            )
        create_user_model.email = create_user_schema.email
        create_user_model.first_name = create_user_schema.first_name
        create_user_model.last_name = create_user_schema.last_name

        hash_password = get_password_hash(create_user_schema.password)
        create_user_model.hashed_password = hash_password

        session.add(create_user_model)
        session.commit()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASHING_ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=401,
        detail=FETCH_USER_RESPONSES[401]["description"],
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASHING_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail=FETCH_USER_RESPONSES[401]["description"])
    return current_user


@router.post("/token", status_code=200, response_model=Token, responses=LOGIN_RESPONSES)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail=LOGIN_RESPONSES[401]["description"],
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
