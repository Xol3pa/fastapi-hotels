


async def test_create_facility(ac):
    response = await ac.post(
        "/facilities",
        json={
          "title": "Гриль и беседка",
        },
    )

    assert response.status_code in [200, 201]


async def test_get_all_facilities(ac):
    response = await ac.get(
        "/facilities",
    )

    # assert response.json() is not None

    assert response.status_code in [200, 201]
