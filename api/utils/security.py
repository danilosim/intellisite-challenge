import logging
from datetime import datetime, timedelta
from typing import Optional

from config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.db import User as UserDB
from models.routers import TokenData, UserInDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthException(Exception):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


async def get_user(username: str):
    user = None
    try:
        user = await UserDB.find_one(UserDB.username == username)
    except Exception:
        logging.exception("Error retrieving user")
    if user:
        return UserInDB(username=user.username, hashed_password=user.password, role=user.role)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await get_user(username=token_data.username)

    if not user:
        raise credentials_exception

    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if user and verify_password(password, user.hashed_password):
        return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt
    except Exception:
        logging.exception("Error creating access token")
        raise AuthException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Error creating access token",
        )
