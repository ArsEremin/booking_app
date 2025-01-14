from fastapi import APIRouter, HTTPException

from users.auth import get_password_hash
from users.schemas import UserRegisterSchema
from users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)


@router.post("/register")
async def register_user(user_data: UserRegisterSchema):
    existing_user = await UserService.get_by_filter(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500)
    hashed_password = get_password_hash(user_data.password)
    await UserService.add_row(email=user_data.email, hashed_password=hashed_password)
