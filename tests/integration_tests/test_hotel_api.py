from httpx import AsyncClient


async def test_get_hotels(async_client: AsyncClient):
    params = {"location": "Алтай", "date_from": "2023-05-30", "date_to": "2023-06-30"}
    response = await async_client.get(url="/v1/hotels", params=params)
    assert response.status_code == 200 and len(response.json()) == 3
