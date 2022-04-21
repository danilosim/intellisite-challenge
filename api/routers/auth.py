from datetime import timedelta

from config import settings
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.routers import Token, User
from utils.security import AuthException, authenticate_user, create_access_token, get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "NOT FOUND"}},
)


@auth_router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    try:
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/refresh", response_model=Token)
async def refresh(current_user: User = Depends(get_current_user)):
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    try:
        access_token = create_access_token(data={"sub": current_user.username}, expires_delta=access_token_expires)
    except AuthException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=access_token, token_type="bearer")
