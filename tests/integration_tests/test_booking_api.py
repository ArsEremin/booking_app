import pytest
from httpx import AsyncClient


class TestBookingAPI:
    @pytest.mark.parametrize(
        "room_id, date_from, date_to, repeat_num, status_code",
        [
            (4, "2024-05-01", "2024-05-15", 8, 201),
            (4, "2024-05-01", "2024-05-15", 2, 409)
        ]
    )
    async def test_add_booking(
        self,
        auth_client: AsyncClient,
        room_id,
        date_from,
        date_to,
        repeat_num,
        status_code
    ):
        cur_bookings_num = 1
        for _ in range(repeat_num):
            response = await auth_client.post(
                url="/bookings",
                params={
                    "room_id": room_id,
                    "date_from": date_from,
                    "date_to": date_to,
                }
            )
            assert response.status_code == status_code

            cur_bookings_num += 1
            response = await auth_client.get("/bookings")
            if status_code == 201:
                assert len(response.json()) == cur_bookings_num

    async def test_delete_booking(self, auth_client: AsyncClient):
        bookings = await auth_client.get("/bookings")
        assert bookings.status_code == 200

        for booking in bookings.json():
            response = await auth_client.delete(f"/bookings/{booking['id']}")
            assert response.status_code == 204

        bookings = await auth_client.get("/bookings")
        assert bookings.status_code == 200 and len(bookings.json()) == 0
