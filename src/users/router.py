from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import InvalidAuthDataException, UserExistsException
from src.users.auth import auth_user, create_access_token, get_password_hash
from src.users.dependencies import get_current_user
from src.users.models import User
from src.users.schemas import UserAuthSchema
from src.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: UserAuthSchema
):
    existing_user = await UserService.get_by_filter(session, email=user_data.email)
    if existing_user:
        raise UserExistsException
    hashed_password = get_password_hash(user_data.password)
    await UserService.add_row(session, email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_async_session)],
    user_data: Annotated[
        UserAuthSchema,
        Body(
            openapi_examples={
                "Ivanov": {
                    "summary": "Ivanov data",
                    "value": {
                        "email": "ivanov@gmail.com",
                        "password": "123"
                    }
                },
                "Petrov": {
                    "summary": "Petrov data",
                    "value": {
                        "email": "petrov@gmail.com",
                        "password": "password123"
                    }
                }
            }
        )
    ]
):
    user = await auth_user(session, user_data.email, user_data.password)
    if not user:
        raise InvalidAuthDataException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def get_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
