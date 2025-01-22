import pytest
from httpx import AsyncClient


class TestUsersAPI:
    @property
    def get_url(self):
        return "/v1/users"

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("test@test.com", "123", 201),
            ("test@test.com", "1234", 409),
            ("abcde", "12345", 422)
        ]
    )
    async def test_register_user(self, async_client: AsyncClient, email, password, status_code):
        response = await async_client.post(
            url=f"{self.get_url}/register",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("fedor@moloko.ru", "fedor", 200),
            ("sharik@moloko.ru", "sharik", 200),
            ("invalid@invalid.ru", "invalid", 401)
        ]
    )
    async def test_login_user(self, async_client: AsyncClient, email, password, status_code):
        response = await async_client.post(
            url=f"{self.get_url}/login",
            json={
                "email": email,
                "password": password
            }
        )
        assert response.status_code == status_code
