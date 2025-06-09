from datetime import date, timedelta


async def test_create_booking(auth_ac, db):
    room_id = (await db.rooms.get_all())[0].id
    today = date.today()
    date_from = today + timedelta(days=30)
    date_to = date_from + timedelta(days=1)

    response = await auth_ac.post(
        "/bookings",
        json={
            'room_id': room_id,
            "date_from": str(date_from),
            "date_to": str(date_to),
        }
    )

    res = response.json()
    print(res)

    assert response.status_code in [200, 201]
    assert res["success"] == True
    assert "data" in res
    assert isinstance(res["data"], dict)