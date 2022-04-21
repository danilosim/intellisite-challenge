from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.db import User as UserDBModel
from models.routers import NewUserModel, User
from passlib.context import CryptContext
from utils.security import get_current_user, pwd_context

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "NOT FOUND"}},
)


@users_router.get("/me", response_model=User)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@users_router.post("/")
async def create_user(new_user: NewUserModel, current_user: User = Depends(get_current_user)):
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmins can create users",
            headers={"WWW-Authenticate": "Bearer"},
        )

    existing_user = await UserDBModel.find_one(UserDBModel.username == new_user.username)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )

    await UserDBModel(
        username=new_user.username, password=pwd_context.hash(new_user.password), role=new_user.role
    ).insert()
    return Response()
