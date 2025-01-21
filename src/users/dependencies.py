from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_async_session
from src.exceptions import InvalidTokenException, TokenExpiredException
from src.users.service import UserService


def get_token(booking_access_token: Annotated[str | None, Cookie()] = None):
    if not booking_access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return booking_access_token


async def get_current_user(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    token: Annotated[str, Depends(get_token)]
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.HASH_ALG0
        )
    except jwt.exceptions.PyJWTError:
        raise InvalidTokenException
    expire: str = payload.get("exp")
    user_id: str = payload.get("sub")
    if not expire or not user_id:
        raise InvalidTokenException
    if int(expire) < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException
    user = await UserService.get_by_id(session, int(user_id))
    if not user:
        raise InvalidTokenException
    return user
