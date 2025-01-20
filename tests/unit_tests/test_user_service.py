import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.service import UserService


class TestUserService:
    @pytest.mark.parametrize(
        "user_id, email, is_exist",
        [
            (1, "fedor@moloko.ru", True),
            (2, "sharik@moloko.ru", True),
            (333, "invalid@invalid.com", False)
        ]
    )
    async def test_get_user_by_id(self, session: AsyncSession, user_id, email, is_exist):
        user = await UserService.get_by_id(session, user_id)
        if is_exist:
            assert user and user.id == user_id and user.email == email
        else:
            assert not user
