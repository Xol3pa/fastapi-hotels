


async def test_get_all(ac):
    response = await ac.get(
        '/hotels',
        params={
            'date_from': '2025-03-01',
            'date_to': '2025-03-31'
        }
    )

    assert response.status_code == 200