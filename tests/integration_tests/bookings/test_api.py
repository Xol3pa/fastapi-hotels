import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-06-15", "2025-06-16", 200),
        (1, "2025-06-15", "2025-06-16", 200),
        (1, "2025-06-15", "2025-06-16", 200),
        (1, "2025-06-15", "2025-06-16", 200),
        (1, "2025-06-15", "2025-06-16", 200),
        (1, "2025-06-15", "2025-06-16", 409),
        (1, "2025-06-17", "2025-06-18", 200),
    ]
)
async def test_create_booking(
        room_id, date_from, date_to, status_code,
        auth_ac, db
):
    response = await auth_ac.post(
        "/bookings",
        json={
            'room_id': room_id,
            "date_from": str(date_from),
            "date_to": str(date_to),
        }
    )

    res = response.json()

    assert response.status_code == status_code
    if status_code == 200:
        assert res["success"] == True
        assert "data" in res
        assert isinstance(res["data"], dict)


async def test_cleanup_after_create_booking_tests(db):
    """Очистка после серии тестов test_create_booking"""
    await db.bookings.delete(force_delete_all=True)
    await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, count_bookings",
    [
        (1, "2025-06-15", "2025-06-16", 200, 1),
        (1, "2025-06-15", "2025-06-16", 200, 2),
        (1, "2025-06-15", "2025-06-16", 200, 3),
    ]
)
async def test_add_and_get_bookings(
        room_id, date_from, date_to, status_code, count_bookings,
        auth_ac
):
    response_create = await auth_ac.post(
        "/bookings",
        json={
            'room_id': room_id,
            "date_from": str(date_from),
            "date_to": str(date_to),
        }
    )

    assert response_create.status_code == status_code

    response_get_bookings = await auth_ac.get("/bookings/me")
    res = response_get_bookings.json()

    assert response_get_bookings.status_code == status_code
    assert len(res) == count_bookings